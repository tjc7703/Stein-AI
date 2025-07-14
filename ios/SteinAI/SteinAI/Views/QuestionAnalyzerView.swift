import SwiftUI
import Speech
import AVFoundation

struct QuestionAnalyzerView: View {
    @EnvironmentObject var questionStore: QuestionStore
    @EnvironmentObject var settingsStore: SettingsStore
    
    @State private var questionText = ""
    @State private var isAnalyzing = false
    @State private var isRecording = false
    @State private var showAnalysisResult = false
    @State private var currentAnalysis: AnalysisResult?
    @State private var showError = false
    @State private var errorMessage = ""
    
    @StateObject private var speechRecognizer = SpeechRecognizer()
    
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                headerView
                inputSection
                analysisSection
                quickActionsSection
                Spacer()
            }
            .padding()
            .navigationTitle("Stein AI")
            .navigationBarTitleDisplayMode(.large)
            .sheet(isPresented: $showAnalysisResult) {
                if let analysis = currentAnalysis {
                    AnalysisResultView(analysis: analysis)
                }
            }
            .alert("오류", isPresented: $showError) {
                Button("확인") { }
            } message: {
                Text(errorMessage)
            }
        }
    }
    
    // MARK: - Header View
    private var headerView: some View {
        VStack(spacing: 12) {
            // Stein AI 로고/아이콘
            Image(systemName: "brain.head.profile")
                .font(.system(size: 60))
                .foregroundColor(.steinBlue)
                .background(
                    Circle()
                        .fill(Color.steinBlue.opacity(0.1))
                        .frame(width: 100, height: 100)
                )
            
            Text("안녕하세요, Stein님!")
                .font(.title2)
                .fontWeight(.semibold)
            
            Text("무엇을 도와드릴까요?")
                .font(.subheadline)
                .foregroundColor(.secondary)
        }
    }
    
    // MARK: - Input Section
    private var inputSection: some View {
        VStack(spacing: 16) {
            // 텍스트 입력 영역
            VStack(alignment: .leading, spacing: 8) {
                HStack {
                    Text("질문 입력")
                        .font(.headline)
                    Spacer()
                    if speechRecognizer.isAvailable {
                        Button(action: toggleRecording) {
                            Image(systemName: isRecording ? "mic.fill" : "mic")
                                .foregroundColor(isRecording ? .red : .steinBlue)
                                .font(.title2)
                        }
                        .disabled(isAnalyzing)
                    }
                }
                
                TextEditor(text: $questionText)
                    .frame(minHeight: 100)
                    .padding(12)
                    .background(Color(.systemGray6))
                    .cornerRadius(12)
                    .overlay(
                        RoundedRectangle(cornerRadius: 12)
                            .stroke(Color.steinBlue.opacity(0.3), lineWidth: 1)
                    )
                    .onChange(of: speechRecognizer.transcript) { newValue in
                        if !newValue.isEmpty {
                            questionText = newValue
                        }
                    }
            }
            
            // 분석 버튼
            Button(action: analyzeQuestion) {
                HStack {
                    if isAnalyzing {
                        ProgressView()
                            .scaleEffect(0.9)
                            .tint(.white)
                    } else {
                        Image(systemName: "brain.head.profile")
                    }
                    Text(isAnalyzing ? "분석 중..." : "스마트 분석")
                        .fontWeight(.semibold)
                }
                .frame(maxWidth: .infinity)
                .frame(height: 50)
                .background(questionText.isEmpty ? Color.gray : Color.steinBlue)
                .foregroundColor(.white)
                .cornerRadius(25)
            }
            .disabled(questionText.isEmpty || isAnalyzing)
        }
    }
    
    // MARK: - Analysis Section
    private var analysisSection: some View {
        Group {
            if let analysis = currentAnalysis {
                VStack(alignment: .leading, spacing: 12) {
                    Text("분석 결과")
                        .font(.headline)
                    
                    AnalysisPreviewCard(analysis: analysis)
                        .onTapGesture {
                            showAnalysisResult = true
                        }
                }
            }
        }
    }
    
    // MARK: - Quick Actions
    private var quickActionsSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("빠른 작업")
                .font(.headline)
            
            LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 2), spacing: 12) {
                QuickActionCard(
                    icon: "book.fill",
                    title: "학습 히스토리",
                    color: .steinGreen
                ) {
                    // 학습 히스토리로 이동
                }
                
                QuickActionCard(
                    icon: "chart.bar.fill",
                    title: "성장 통계",
                    color: .steinPurple
                ) {
                    // 통계로 이동
                }
                
                QuickActionCard(
                    icon: "doc.text.fill",
                    title: "논문 학습",
                    color: .steinOrange
                ) {
                    // 논문 학습으로 이동
                }
                
                QuickActionCard(
                    icon: "gear",
                    title: "설정",
                    color: .gray
                ) {
                    // 설정으로 이동
                }
            }
        }
    }
    
    // MARK: - Actions
    private func analyzeQuestion() {
        guard !questionText.isEmpty else { return }
        
        isAnalyzing = true
        
        Task {
            do {
                let analysis = try await SteinAPIManager.shared.analyzeQuestionSmart(
                    question: questionText,
                    sessionHistory: questionStore.recentQuestions
                )
                
                await MainActor.run {
                    currentAnalysis = analysis
                    questionStore.addQuestion(questionText, analysis: analysis)
                    isAnalyzing = false
                    
                    // 햅틱 피드백
                    let impact = UIImpactFeedbackGenerator(style: .medium)
                    impact.impactOccurred()
                }
            } catch {
                await MainActor.run {
                    errorMessage = error.localizedDescription
                    showError = true
                    isAnalyzing = false
                }
            }
        }
    }
    
    private func toggleRecording() {
        if isRecording {
            speechRecognizer.stopRecording()
        } else {
            speechRecognizer.startRecording()
        }
        isRecording.toggle()
    }
}

// MARK: - Analysis Preview Card
struct AnalysisPreviewCard: View {
    let analysis: AnalysisResult
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    Text("의도: \(analysis.intent.displayName)")
                        .font(.subheadline)
                        .fontWeight(.medium)
                    
                    Text("우선순위: \(Int(analysis.priorityScore))점")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                
                Spacer()
                
                VStack(alignment: .trailing, spacing: 4) {
                    urgencyBadge
                    Text(analysis.estimatedTime)
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
            
            Text(analysis.reasoning)
                .font(.caption)
                .lineLimit(2)
                .foregroundColor(.secondary)
            
            HStack {
                Spacer()
                Text("자세히 보기")
                    .font(.caption)
                    .foregroundColor(.steinBlue)
                Image(systemName: "chevron.right")
                    .font(.caption)
                    .foregroundColor(.steinBlue)
            }
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(12)
    }
    
    private var urgencyBadge: some View {
        Text(analysis.urgency.displayName)
            .font(.caption2)
            .fontWeight(.semibold)
            .padding(.horizontal, 8)
            .padding(.vertical, 4)
            .background(analysis.urgency.color.opacity(0.2))
            .foregroundColor(analysis.urgency.color)
            .cornerRadius(8)
    }
}

// MARK: - Quick Action Card
struct QuickActionCard: View {
    let icon: String
    let title: String
    let color: Color
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            VStack(spacing: 8) {
                Image(systemName: icon)
                    .font(.title2)
                    .foregroundColor(color)
                
                Text(title)
                    .font(.caption)
                    .fontWeight(.medium)
                    .multilineTextAlignment(.center)
            }
            .frame(maxWidth: .infinity)
            .frame(height: 80)
            .background(Color(.systemGray6))
            .cornerRadius(12)
        }
        .buttonStyle(PlainButtonStyle())
    }
}

// MARK: - Preview
struct QuestionAnalyzerView_Previews: PreviewProvider {
    static var previews: some View {
        QuestionAnalyzerView()
            .environmentObject(QuestionStore())
            .environmentObject(SettingsStore())
    }
} 