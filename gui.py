"""
===================================================================
PREMIUM PyQt5 GUI — Smart Resume & Career Intelligence System
===================================================================
Award-winning desktop application with dark theme, animated
score displays, tabbed dashboard, and embedded chart viewer.
===================================================================
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QFileDialog, QProgressBar,
    QTabWidget, QScrollArea, QFrame, QGridLayout, QSplitter,
    QStackedWidget, QMessageBox, QSizePolicy
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize
from PyQt5.QtGui import QFont, QPixmap, QIcon, QPalette, QColor

from gui_styles import (
    MAIN_STYLESHEET, CARD_STYLE, SCORE_CARD_STYLE,
    HEADER_STYLE, SUBHEADER_STYLE,
    SKILL_PILL_PRESENT, SKILL_PILL_MISSING
)
from modules.input_module import load_resume
from modules.nlp_module import preprocess_resume
from modules.feature_module import create_tfidf_vectors, get_top_keywords
from modules.job_data_module import get_job_database
from modules.matching_module import calculate_similarity
from modules.analysis_module import analyze_results
from modules.storage_module import save_results, generate_analysis_id
from modules.visualization_module import generate_all_charts


class AnalysisWorker(QThread):
    """Background thread to run the analysis pipeline."""
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, resume_source):
        super().__init__()
        self.resume_source = resume_source

    def run(self):
        try:
            self.progress.emit(5, "Loading resume...")
            raw_text = load_resume(self.resume_source)

            self.progress.emit(15, "NLP preprocessing...")
            nlp_result = preprocess_resume(raw_text)

            self.progress.emit(35, "Loading job database...")
            jobs = get_job_database()
            job_texts = [j['description'] for j in jobs]

            self.progress.emit(50, "TF-IDF vectorization...")
            tfidf = create_tfidf_vectors(nlp_result['processed_text'], job_texts)
            top_kw = get_top_keywords(tfidf['vectorizer'], tfidf['resume_vector'], 10)

            self.progress.emit(65, "Computing similarity scores...")
            matches = calculate_similarity(tfidf['resume_vector'], tfidf['job_vectors'], jobs, nlp_result['skills'])

            self.progress.emit(78, "Analyzing skill gaps...")
            analysis = analyze_results(matches, nlp_result['skills'])

            self.progress.emit(88, "Saving results...")
            aid = generate_analysis_id(raw_text)
            saved = save_results(aid, analysis, raw_text)

            self.progress.emit(95, "Generating visualizations...")
            charts = generate_all_charts(analysis, aid)

            self.progress.emit(100, "Complete!")
            self.finished.emit({
                'analysis_id': aid, 'analysis': analysis,
                'charts': charts, 'saved_files': saved,
                'nlp_result': nlp_result, 'top_keywords': top_kw
            })
        except Exception as e:
            self.error.emit(str(e))


def make_card(parent=None):
    """Create a styled card frame."""
    card = QFrame(parent)
    card.setStyleSheet(CARD_STYLE)
    return card


def make_score_label(value, suffix="%", size=42, color="#00d4ff"):
    """Create a large animated score label."""
    lbl = QLabel(f"{value}{suffix}")
    lbl.setAlignment(Qt.AlignCenter)
    lbl.setStyleSheet(f"font-size:{size}px; font-weight:bold; color:{color}; background:transparent;")
    return lbl


def make_section_title(text):
    """Create a section title label."""
    lbl = QLabel(text)
    lbl.setStyleSheet("font-size:18px; font-weight:bold; color:#00d4ff; background:transparent; padding:8px 0;")
    return lbl


class UploadPage(QWidget):
    """Page 1: Resume upload / paste interface."""
    analyze_requested = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # Outer scroll wrapper — prevents ANY clipping
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        outer.addWidget(scroll)

        inner = QWidget()
        scroll.setWidget(inner)

        layout = QVBoxLayout(inner)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(18)
        layout.setContentsMargins(80, 40, 80, 40)

        # Title
        title = QLabel("AI-Powered Resume Analyzer")
        title.setStyleSheet(
            "font-size:30px; font-weight:bold; color:#00d4ff; background:transparent;"
        )
        title.setAlignment(Qt.AlignCenter)
        title.setWordWrap(True)
        layout.addWidget(title)

        sub = QLabel(
            "Upload your resume or paste text below to get career intelligence insights"
        )
        sub.setStyleSheet("font-size:14px; color:#888; background:transparent;")
        sub.setAlignment(Qt.AlignCenter)
        sub.setWordWrap(True)
        layout.addWidget(sub)

        layout.addSpacing(10)

        # Drop Zone Card — dashed border, fixed min height so text never clips
        upload_card = QFrame()
        upload_card.setMinimumHeight(200)
        upload_card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 #1a1a2e, stop:1 #151528);
                border: 2px dashed #7c3aed;
                border-radius: 14px;
            }
        """)
        uc_layout = QVBoxLayout(upload_card)
        uc_layout.setAlignment(Qt.AlignCenter)
        uc_layout.setSpacing(12)
        uc_layout.setContentsMargins(30, 25, 30, 25)

        icon_lbl = QLabel("DROP YOUR RESUME FILE HERE")
        icon_lbl.setStyleSheet(
            "font-size:20px; font-weight:bold; color:#7c3aed;"
            "background:transparent; letter-spacing:2px;"
        )
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setWordWrap(True)
        uc_layout.addWidget(icon_lbl)

        hint = QLabel("Supports .txt files  |  Or paste text in the box below")
        hint.setStyleSheet("color:#555; font-size:12px; background:transparent;")
        hint.setAlignment(Qt.AlignCenter)
        hint.setWordWrap(True)
        uc_layout.addWidget(hint)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        self.upload_btn = QPushButton("  Browse File  ")
        self.upload_btn.setMinimumHeight(40)
        self.upload_btn.clicked.connect(self.browse_file)
        btn_row.addWidget(self.upload_btn)

        self.sample_btn = QPushButton("  Use Sample Resume  ")
        self.sample_btn.setObjectName("secondaryBtn")
        self.sample_btn.setMinimumHeight(40)
        self.sample_btn.clicked.connect(self.use_sample)
        btn_row.addWidget(self.sample_btn)
        uc_layout.addLayout(btn_row)

        layout.addWidget(upload_card)

        # OR divider
        divider = QLabel("— OR PASTE RESUME TEXT BELOW —")
        divider.setStyleSheet(
            "color:#444; font-size:11px; letter-spacing:1px; background:transparent;"
        )
        divider.setAlignment(Qt.AlignCenter)
        layout.addWidget(divider)

        # Text input
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText(
            "Paste your full resume text here...\n\n"
            "Example:\n  John Doe  |  Python Developer\n"
            "  Skills: Python, Django, Machine Learning, SQL..."
        )
        self.text_edit.setMinimumHeight(200)
        self.text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.text_edit)

        # Analyze button
        self.analyze_btn = QPushButton("  ANALYZE RESUME  ")
        self.analyze_btn.setMinimumHeight(52)
        self.analyze_btn.setMinimumWidth(260)
        self.analyze_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #00d4ff, stop:1 #7c3aed);
                font-size:16px; font-weight:bold;
                padding:14px 50px; border-radius:10px; color:white;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #33dfff, stop:1 #9b5de5);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #0099cc, stop:1 #5b21b6);
            }
        """)
        self.analyze_btn.clicked.connect(self.on_analyze)
        layout.addWidget(self.analyze_btn, alignment=Qt.AlignCenter)

        layout.addSpacing(30)
        self.selected_file = None

    def reset(self):
        """Clear previous input so a fresh resume can be loaded."""
        self.selected_file = None
        self.text_edit.clear()

    def browse_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Resume", "", "Text Files (*.txt);;All Files (*)")
        if path:
            self.selected_file = path
            self.text_edit.setPlainText(f"[File selected: {os.path.basename(path)}]")

    def use_sample(self):
        from config import SAMPLE_DIR
        sample = os.path.join(SAMPLE_DIR, "sample_resume.txt")
        if os.path.exists(sample):
            self.selected_file = sample
            with open(sample, 'r') as f:
                self.text_edit.setPlainText(f.read())
        else:
            QMessageBox.warning(self, "Error", "Sample resume not found!")

    def on_analyze(self):
        if self.selected_file and os.path.exists(self.selected_file):
            self.analyze_requested.emit(self.selected_file)
        elif self.text_edit.toPlainText().strip() and not self.text_edit.toPlainText().startswith("[File"):
            self.analyze_requested.emit(self.text_edit.toPlainText())
        else:
            QMessageBox.warning(self, "No Input", "Please upload a file or paste resume text.")


class DashboardPage(QWidget):
    """Page 2: Results dashboard with tabs."""
    go_back = pyqtSignal()   # Signal to return to upload page

    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 10, 20, 10)
        self._results_dir = None

    def populate(self, results):
        """Fill dashboard with analysis results."""
        # Clear existing
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        analysis = results['analysis']
        charts = results['charts']

        # Store results dir for open folder button
        if results.get('saved_files'):
            first_file = list(results['saved_files'].values())[0]
            self._results_dir = os.path.dirname(first_file)

        # Header row
        header_row = QHBoxLayout()
        title = QLabel("Career Intelligence Dashboard")
        title.setStyleSheet(HEADER_STYLE)
        header_row.addWidget(title)
        header_row.addStretch()
        aid_lbl = QLabel(f"ID: {results['analysis_id']}")
        aid_lbl.setStyleSheet("color:#666; font-size:11px; background:transparent;")
        header_row.addWidget(aid_lbl)

        # Open Results Folder button
        open_btn = QPushButton("  Open Results Folder  ")
        open_btn.setObjectName("secondaryBtn")
        open_btn.setFixedHeight(36)
        open_btn.clicked.connect(self._open_results)
        header_row.addWidget(open_btn)

        # Analyze New Resume button
        back_btn = QPushButton("  + Analyze New Resume  ")
        back_btn.setFixedHeight(36)
        back_btn.clicked.connect(self.go_back.emit)
        header_row.addWidget(back_btn)

        h_widget = QWidget()
        h_widget.setLayout(header_row)
        self.main_layout.addWidget(h_widget)

        # Score cards row
        scores_widget = QWidget()
        scores_layout = QHBoxLayout(scores_widget)
        scores_layout.setSpacing(16)

        # Card 1: Resume Strength
        c1 = make_card()
        c1_l = QVBoxLayout(c1)
        c1_l.addWidget(QLabel("RESUME STRENGTH"))
        c1_l.addWidget(make_score_label(analysis['resume_strength'], "/100", 38, "#00d4ff"))
        scores_layout.addWidget(c1)

        # Card 2: Top Match
        c2 = make_card()
        c2_l = QVBoxLayout(c2)
        c2_l.addWidget(QLabel("TOP MATCH"))
        c2_l.addWidget(make_score_label(analysis['top_match'], "%", 38, "#10b981"))
        top_job = QLabel(analysis['match_results'][0]['title'])
        top_job.setStyleSheet("color:#10b981; font-size:13px; background:transparent;")
        top_job.setAlignment(Qt.AlignCenter)
        c2_l.addWidget(top_job)
        scores_layout.addWidget(c2)

        # Card 3: Skills Found
        c3 = make_card()
        c3_l = QVBoxLayout(c3)
        c3_l.addWidget(QLabel("SKILLS FOUND"))
        c3_l.addWidget(make_score_label(analysis['total_skills'], "", 38, "#f59e0b"))
        cats = QLabel(f"across {len(analysis['resume_skills'])} categories")
        cats.setStyleSheet("color:#f59e0b; font-size:12px; background:transparent;")
        cats.setAlignment(Qt.AlignCenter)
        c3_l.addWidget(cats)
        scores_layout.addWidget(c3)

        # Card 4: Avg Match
        c4 = make_card()
        c4_l = QVBoxLayout(c4)
        c4_l.addWidget(QLabel("AVG MATCH"))
        c4_l.addWidget(make_score_label(analysis['avg_match'], "%", 38, "#7c3aed"))
        scores_layout.addWidget(c4)

        self.main_layout.addWidget(scores_widget)

        # Tabs
        tabs = QTabWidget()
        tabs.setMinimumHeight(400)

        # Tab 1: Charts
        charts_tab = QWidget()
        ct_layout = QVBoxLayout(charts_tab)
        ct_scroll = QScrollArea()
        ct_scroll.setWidgetResizable(True)
        ct_inner = QWidget()
        ct_inner_layout = QVBoxLayout(ct_inner)

        for name, path in charts.items():
            if path and os.path.exists(path):
                lbl = QLabel()
                pixmap = QPixmap(path)
                scaled = pixmap.scaledToWidth(750, Qt.SmoothTransformation)
                lbl.setPixmap(scaled)
                lbl.setAlignment(Qt.AlignCenter)
                ct_inner_layout.addWidget(lbl)
                ct_inner_layout.addSpacing(10)

        ct_scroll.setWidget(ct_inner)
        ct_layout.addWidget(ct_scroll)
        tabs.addTab(charts_tab, "  Charts  ")

        # Tab 2: Job Matches
        jobs_tab = QWidget()
        jt_layout = QVBoxLayout(jobs_tab)
        jt_scroll = QScrollArea()
        jt_scroll.setWidgetResizable(True)
        jt_inner = QWidget()
        jt_inner_layout = QVBoxLayout(jt_inner)

        for job in analysis['match_results']:
            card = make_card()
            cl = QHBoxLayout(card)
            rank_lbl = QLabel(f"#{job['rank']}")
            rank_lbl.setStyleSheet("font-size:24px; font-weight:bold; color:#7c3aed; background:transparent; min-width:50px;")
            cl.addWidget(rank_lbl)

            info = QVBoxLayout()
            jtitle = QLabel(f"{job['title']}  ({job['category']})")
            jtitle.setStyleSheet("font-size:15px; font-weight:bold; background:transparent;")
            info.addWidget(jtitle)
            score_color = "#10b981" if job['match_score'] >= 70 else "#f59e0b" if job['match_score'] >= 45 else "#ef4444"
            jsc = QLabel(f"Match: {job['match_score']}%  |  Cosine: {job['cosine_raw']}")
            jsc.setStyleSheet(f"color:{score_color}; font-size:13px; background:transparent;")
            info.addWidget(jsc)
            cl.addLayout(info)
            cl.addStretch()

            jt_inner_layout.addWidget(card)

        jt_scroll.setWidget(jt_inner)
        jt_layout.addWidget(jt_scroll)
        tabs.addTab(jobs_tab, "  Job Matches  ")

        # Tab 3: Skill Gaps
        gaps_tab = QWidget()
        gt_layout = QVBoxLayout(gaps_tab)
        gt_scroll = QScrollArea()
        gt_scroll.setWidgetResizable(True)
        gt_inner = QWidget()
        gt_inner_layout = QVBoxLayout(gt_inner)

        for gap in analysis['skill_gap_analysis']:
            card = make_card()
            gcl = QVBoxLayout(card)
            gt_title = QLabel(f"{gap['title']}  —  Coverage: {gap['skill_coverage']}%")
            gt_title.setStyleSheet("font-size:14px; font-weight:bold; background:transparent;")
            gcl.addWidget(gt_title)

            # Present skills
            if gap['present_skills']:
                p_row = QHBoxLayout()
                p_row.addWidget(QLabel("Have:"))
                for sk in gap['present_skills']:
                    pill = QLabel(sk)
                    pill.setStyleSheet(SKILL_PILL_PRESENT)
                    p_row.addWidget(pill)
                p_row.addStretch()
                gcl.addLayout(p_row)

            # Missing skills
            if gap['missing_skills']:
                m_row = QHBoxLayout()
                m_row.addWidget(QLabel("Need:"))
                for sk in gap['missing_skills']:
                    pill = QLabel(sk)
                    pill.setStyleSheet(SKILL_PILL_MISSING)
                    m_row.addWidget(pill)
                m_row.addStretch()
                gcl.addLayout(m_row)

            gt_inner_layout.addWidget(card)

        gt_scroll.setWidget(gt_inner)
        gt_layout.addWidget(gt_scroll)
        tabs.addTab(gaps_tab, "  Skill Gaps  ")

        # Tab 4: Recommendations
        rec_tab = QWidget()
        rt_layout = QVBoxLayout(rec_tab)
        for rec in analysis['recommendations']:
            card = make_card()
            rcl = QVBoxLayout(card)
            rec_lbl = QLabel(f"  {rec}")
            rec_lbl.setWordWrap(True)
            rec_lbl.setStyleSheet("font-size:14px; line-height:1.6; background:transparent; padding:8px;")
            rcl.addWidget(rec_lbl)
            rt_layout.addWidget(card)
        rt_layout.addStretch()
        tabs.addTab(rec_tab, "  Recommendations  ")

        self.main_layout.addWidget(tabs)

    def _open_results(self):
        """Open the results folder in Windows Explorer."""
        import subprocess
        if self._results_dir and os.path.isdir(self._results_dir):
            subprocess.Popen(f'explorer "{self._results_dir}"')
        else:
            QMessageBox.information(self, "Results", "Results folder not found.")


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Resume & Career Intelligence System")
        self.setMinimumSize(1000, 700)
        self.setStyleSheet(MAIN_STYLESHEET)

        # Stacked pages
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Page 0: Upload
        self.upload_page = UploadPage()
        self.upload_page.analyze_requested.connect(self.start_analysis)
        self.stack.addWidget(self.upload_page)

        # Page 1: Loading
        self.loading_page = QWidget()
        ll = QVBoxLayout(self.loading_page)
        ll.setAlignment(Qt.AlignCenter)
        self.loading_label = QLabel("Analyzing your resume...")
        self.loading_label.setStyleSheet("font-size:20px; font-weight:bold; color:#00d4ff; background:transparent;")
        self.loading_label.setAlignment(Qt.AlignCenter)
        ll.addWidget(self.loading_label)
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumWidth(500)
        self.progress_bar.setMaximumWidth(600)
        ll.addWidget(self.progress_bar, alignment=Qt.AlignCenter)
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color:#888; font-size:13px; background:transparent;")
        self.status_label.setAlignment(Qt.AlignCenter)
        ll.addWidget(self.status_label)
        self.stack.addWidget(self.loading_page)

        # Page 2: Dashboard
        self.dashboard_scroll = QScrollArea()
        self.dashboard_scroll.setWidgetResizable(True)
        self.dashboard_page = DashboardPage()
        self.dashboard_page.go_back.connect(self.go_to_upload)
        self.dashboard_scroll.setWidget(self.dashboard_page)
        self.stack.addWidget(self.dashboard_scroll)

    def start_analysis(self, source):
        """Launch analysis in background thread."""
        self.stack.setCurrentIndex(1)
        self.progress_bar.setValue(0)

        self.worker = AnalysisWorker(source)
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_progress(self, value, msg):
        self.progress_bar.setValue(value)
        self.status_label.setText(msg)

    def on_finished(self, results):
        self.dashboard_page.populate(results)
        self.stack.setCurrentIndex(2)

    def go_to_upload(self):
        """Return to upload page and clear previous input."""
        self.upload_page.reset()
        self.stack.setCurrentIndex(0)

    def on_error(self, msg):
        QMessageBox.critical(self, "Error", f"Analysis failed:\n{msg}")
        self.stack.setCurrentIndex(0)


def launch_gui():
    """Entry point for the PyQt5 GUI."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    # Dark palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(10, 10, 20))
    palette.setColor(QPalette.WindowText, QColor(224, 224, 224))
    palette.setColor(QPalette.Base, QColor(18, 18, 42))
    palette.setColor(QPalette.Text, QColor(224, 224, 224))
    palette.setColor(QPalette.Button, QColor(26, 26, 46))
    palette.setColor(QPalette.ButtonText, QColor(224, 224, 224))
    palette.setColor(QPalette.Highlight, QColor(0, 212, 255))
    app.setPalette(palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    launch_gui()
