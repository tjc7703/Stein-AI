import SwiftUI
import CloudKit

@main
struct SteinAIApp: App {
    @StateObject private var questionStore = QuestionStore()
    @StateObject private var learningStore = LearningStore()
    @StateObject private var settingsStore = SettingsStore()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(questionStore)
                .environmentObject(learningStore)
                .environmentObject(settingsStore)
                .onAppear {
                    setupApp()
                }
        }
    }
    
    private func setupApp() {
        // CloudKit 초기화
        CloudKitManager.shared.initialize()
        
        // 백그라운드 작업 설정
        BackgroundTaskManager.shared.setup()
        
        // 알림 권한 요청
        NotificationManager.shared.requestPermission()
    }
}

// MARK: - Content View
struct ContentView: View {
    @EnvironmentObject var questionStore: QuestionStore
    @EnvironmentObject var learningStore: LearningStore
    @EnvironmentObject var settingsStore: SettingsStore
    
    @State private var selectedTab = 0
    
    var body: some View {
        TabView(selection: $selectedTab) {
            // 메인 질문 분석 탭
            QuestionAnalyzerView()
                .tabItem {
                    Label("분석", systemImage: "brain.head.profile")
                }
                .tag(0)
            
            // 학습 히스토리 탭
            LearningHistoryView()
                .tabItem {
                    Label("학습", systemImage: "book.fill")
                }
                .tag(1)
            
            // 통계 및 성장 탭
            StatsView()
                .tabItem {
                    Label("통계", systemImage: "chart.bar.fill")
                }
                .tag(2)
            
            // 설정 탭
            SettingsView()
                .tabItem {
                    Label("설정", systemImage: "gear")
                }
                .tag(3)
        }
        .accentColor(.steinBlue)
        .onAppear {
            setupTabBarAppearance()
        }
    }
    
    private func setupTabBarAppearance() {
        let appearance = UITabBarAppearance()
        appearance.configureWithOpaqueBackground()
        appearance.backgroundColor = UIColor.systemBackground
        UITabBar.appearance().standardAppearance = appearance
        UITabBar.appearance().scrollEdgeAppearance = appearance
    }
}

// MARK: - Color Extensions
extension Color {
    static let steinBlue = Color(red: 0.2, green: 0.4, blue: 0.9)
    static let steinPurple = Color(red: 0.4, green: 0.2, blue: 0.8)
    static let steinGreen = Color(red: 0.1, green: 0.7, blue: 0.3)
    static let steinOrange = Color(red: 1.0, green: 0.4, blue: 0.0)
}

// MARK: - Preview
struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
            .environmentObject(QuestionStore())
            .environmentObject(LearningStore())
            .environmentObject(SettingsStore())
    }
} 