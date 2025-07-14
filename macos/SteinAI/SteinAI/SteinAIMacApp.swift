import SwiftUI
import Cocoa
import Carbon

@main
struct SteinAIMacApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    @StateObject private var windowManager = WindowManager()
    @StateObject private var questionStore = QuestionStore()
    @StateObject private var settingsStore = SettingsStore()
    
    var body: some Scene {
        // 메인 윈도우 (숨겨진 상태로 시작)
        WindowGroup {
            MainContentView()
                .environmentObject(windowManager)
                .environmentObject(questionStore)
                .environmentObject(settingsStore)
                .frame(minWidth: 800, minHeight: 600)
        }
        .windowResizability(.contentSize)
        .defaultPosition(.center)
        .commands {
            SteinCommands()
        }
        
        // 메뉴바 Extra (항상 표시)
        MenuBarExtra("Stein AI", systemImage: "brain.head.profile") {
            MenuBarContentView()
                .environmentObject(windowManager)
                .environmentObject(questionStore)
                .environmentObject(settingsStore)
        }
        .menuBarExtraStyle(.window)
        
        // 설정 윈도우
        Window("Stein AI 설정", id: "settings") {
            SettingsView()
                .environmentObject(settingsStore)
                .frame(width: 500, height: 400)
        }
        .windowResizability(.contentSize)
    }
}

// MARK: - App Delegate
class AppDelegate: NSObject, NSApplicationDelegate {
    var statusItem: NSStatusItem?
    var globalHotkeyManager: GlobalHotkeyManager?
    
    func applicationDidFinishLaunching(_ notification: Notification) {
        // 앱 시작 시 독에서 숨기기
        NSApp.setActivationPolicy(.accessory)
        
        // 글로벌 단축키 설정 (⌘ + Shift + S)
        setupGlobalHotkey()
        
        // 시작 시 메인 윈도우 숨기기
        hideMainWindow()
        
        print("🚀 Stein AI macOS 앱이 시작되었습니다!")
    }
    
    private func setupGlobalHotkey() {
        globalHotkeyManager = GlobalHotkeyManager()
        globalHotkeyManager?.registerHotkey {
            DispatchQueue.main.async {
                self.toggleQuickAnalysis()
            }
        }
    }
    
    private func hideMainWindow() {
        for window in NSApp.windows {
            if window.title.isEmpty == false && window.title != "Stein AI" {
                continue
            }
            window.close()
        }
    }
    
    private func toggleQuickAnalysis() {
        // 빠른 분석 플로팅 윈도우 토글
        FloatingWindowManager.shared.toggleQuickAnalysis()
    }
}

// MARK: - Main Content View
struct MainContentView: View {
    @EnvironmentObject var windowManager: WindowManager
    @EnvironmentObject var questionStore: QuestionStore
    @EnvironmentObject var settingsStore: SettingsStore
    
    var body: some View {
        NavigationSplitView {
            // 사이드바
            SidebarView()
        } detail: {
            // 메인 콘텐츠
            ContentDetailView()
        }
        .navigationTitle("Stein AI")
        .toolbar {
            ToolbarItem(placement: .navigation) {
                Button(action: toggleSidebar) {
                    Image(systemName: "sidebar.left")
                }
            }
            
            ToolbarItem(placement: .primaryAction) {
                HStack {
                    Button("빠른 분석") {
                        FloatingWindowManager.shared.showQuickAnalysis()
                    }
                    .keyboardShortcut("q", modifiers: [.command])
                    
                    Button("설정") {
                        openSettings()
                    }
                    .keyboardShortcut(",", modifiers: [.command])
                }
            }
        }
    }
    
    private func toggleSidebar() {
        NSApp.keyWindow?.firstResponder?.tryToPerform(#selector(NSSplitViewController.toggleSidebar(_:)), with: nil)
    }
    
    private func openSettings() {
        if let window = NSApp.window(withWindowNumber: 0) {
            window.makeKeyAndOrderFront(nil)
        } else {
            // 설정 윈도우 열기
            NSApp.sendAction(#selector(AppDelegate.openSettings), to: nil, from: nil)
        }
    }
}

// MARK: - Menu Bar Content View
struct MenuBarContentView: View {
    @EnvironmentObject var windowManager: WindowManager
    @EnvironmentObject var questionStore: QuestionStore
    @EnvironmentObject var settingsStore: SettingsStore
    
    @State private var quickQuestion = ""
    
    var body: some View {
        VStack(spacing: 16) {
            // 헤더
            HStack {
                Image(systemName: "brain.head.profile")
                    .foregroundColor(.blue)
                    .font(.title2)
                
                VStack(alignment: .leading) {
                    Text("Stein AI")
                        .font(.headline)
                        .fontWeight(.semibold)
                    
                    Text("안녕하세요, Stein님!")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                
                Spacer()
            }
            
            Divider()
            
            // 빠른 질문 입력
            VStack(alignment: .leading, spacing: 8) {
                Text("빠른 질문")
                    .font(.subheadline)
                    .fontWeight(.medium)
                
                TextField("질문을 입력하세요...", text: $quickQuestion)
                    .textFieldStyle(.roundedBorder)
                    .onSubmit {
                        analyzeQuickQuestion()
                    }
                
                Button("분석하기") {
                    analyzeQuickQuestion()
                }
                .buttonStyle(.borderedProminent)
                .disabled(quickQuestion.isEmpty)
            }
            
            Divider()
            
            // 최근 분석 결과
            VStack(alignment: .leading, spacing: 8) {
                Text("최근 분석")
                    .font(.subheadline)
                    .fontWeight(.medium)
                
                if let recent = questionStore.recentAnalyses.first {
                    RecentAnalysisCard(analysis: recent)
                } else {
                    Text("아직 분석 기록이 없습니다")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
            
            Divider()
            
            // 액션 버튼들
            VStack(spacing: 8) {
                Button("메인 앱 열기") {
                    openMainApp()
                }
                .buttonStyle(.borderless)
                
                Button("플로팅 윈도우") {
                    FloatingWindowManager.shared.showQuickAnalysis()
                }
                .buttonStyle(.borderless)
                
                Button("설정") {
                    openSettings()
                }
                .buttonStyle(.borderless)
                
                Button("종료") {
                    NSApp.terminate(nil)
                }
                .buttonStyle(.borderless)
                .foregroundColor(.red)
            }
        }
        .frame(width: 300)
        .padding()
    }
    
    private func analyzeQuickQuestion() {
        guard !quickQuestion.isEmpty else { return }
        
        Task {
            do {
                let analysis = try await SteinAPIManager.shared.analyzeQuestionSmart(
                    question: quickQuestion,
                    sessionHistory: questionStore.recentQuestions
                )
                
                await MainActor.run {
                    questionStore.addQuestion(quickQuestion, analysis: analysis)
                    quickQuestion = ""
                    
                    // 결과 알림
                    NotificationManager.shared.showAnalysisComplete(analysis: analysis)
                }
            } catch {
                await MainActor.run {
                    // 에러 알림
                    NotificationManager.shared.showError(message: error.localizedDescription)
                }
            }
        }
    }
    
    private func openMainApp() {
        NSApp.setActivationPolicy(.regular)
        NSApp.activate(ignoringOtherApps: true)
        
        // 메인 윈도우 표시
        for window in NSApp.windows {
            if window.title == "Stein AI" {
                window.makeKeyAndOrderFront(nil)
                return
            }
        }
        
        // 새 윈도우 생성
        let contentView = MainContentView()
            .environmentObject(windowManager)
            .environmentObject(questionStore)
            .environmentObject(settingsStore)
        
        let window = NSWindow(
            contentRect: NSRect(x: 0, y: 0, width: 800, height: 600),
            styleMask: [.titled, .closable, .miniaturizable, .resizable],
            backing: .buffered,
            defer: false
        )
        
        window.center()
        window.setFrameAutosaveName("MainWindow")
        window.contentView = NSHostingView(rootView: contentView)
        window.title = "Stein AI"
        window.makeKeyAndOrderFront(nil)
    }
    
    private func openSettings() {
        // 설정 윈도우 열기 로직
    }
}

// MARK: - Recent Analysis Card
struct RecentAnalysisCard: View {
    let analysis: AnalysisResult
    
    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            HStack {
                Text(analysis.intent.displayName)
                    .font(.caption)
                    .fontWeight(.medium)
                
                Spacer()
                
                Text("\(Int(analysis.priorityScore))점")
                    .font(.caption2)
                    .padding(.horizontal, 6)
                    .padding(.vertical, 2)
                    .background(Color.blue.opacity(0.2))
                    .cornerRadius(4)
            }
            
            Text(analysis.reasoning)
                .font(.caption2)
                .lineLimit(2)
                .foregroundColor(.secondary)
        }
        .padding(8)
        .background(Color(.controlBackgroundColor))
        .cornerRadius(6)
    }
}

// MARK: - Global Hotkey Manager
class GlobalHotkeyManager {
    private var hotKeyRef: EventHotKeyRef?
    private var callback: (() -> Void)?
    
    func registerHotkey(callback: @escaping () -> Void) {
        self.callback = callback
        
        let hotKeyID = EventHotKeyID(signature: OSType(0x53544E), id: 1) // 'STN'
        let keyCode = UInt32(kVK_ANSI_S) // S 키
        let modifiers = UInt32(cmdKey | shiftKey) // Cmd + Shift
        
        let eventType = [
            EventTypeSpec(eventClass: OSType(kEventClassKeyboard), eventKind: OSType(kEventHotKeyPressed))
        ]
        
        InstallEventHandler(
            GetApplicationEventTarget(),
            { (handler, event, userData) -> OSStatus in
                if let manager = userData?.assumingMemoryBound(to: GlobalHotkeyManager.self).pointee {
                    manager.callback?()
                }
                return noErr
            },
            1,
            eventType,
            Unmanaged.passUnretained(self).toOpaque(),
            nil
        )
        
        RegisterEventHotKey(
            keyCode,
            modifiers,
            hotKeyID,
            GetApplicationEventTarget(),
            0,
            &hotKeyRef
        )
    }
    
    deinit {
        if let hotKeyRef = hotKeyRef {
            UnregisterEventHotKey(hotKeyRef)
        }
    }
}

// MARK: - Commands
struct SteinCommands: Commands {
    var body: some Commands {
        CommandGroup(replacing: .newItem) {
            Button("빠른 분석") {
                FloatingWindowManager.shared.showQuickAnalysis()
            }
            .keyboardShortcut("n", modifiers: [.command])
        }
        
        CommandGroup(after: .windowArrangement) {
            Button("플로팅 윈도우") {
                FloatingWindowManager.shared.toggleQuickAnalysis()
            }
            .keyboardShortcut("f", modifiers: [.command, .shift])
        }
    }
}

// MARK: - Window Manager
class WindowManager: ObservableObject {
    @Published var currentView: MainView = .analyzer
}

enum MainView {
    case analyzer
    case history
    case stats
    case settings
} 