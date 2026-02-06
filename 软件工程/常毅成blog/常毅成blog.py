import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QGridLayout,
    QListWidget, QListWidgetItem, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class PersonalBlog(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口基本属性
        self.setWindowTitle('常毅成的博客系统')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial, sans-serif;
            }
            .info-label {
                color: #2c3e50;
                font-size: 18px;
                margin: 10px;
            }
            .avatar {
                width: 150px;
                height: 150px;
                border-radius: 50%;
                background-color: #fff;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            .text-area {
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                margin: 20px;
            }
            button {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                margin: 5px;
                transition: background-color 0.3s;
            }
            button:hover {
                background-color: #2980b9;
            }
        """)

        # 创建布局容器
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        # 顶部个人信息区
        topInfoLayout = QHBoxLayout()
        topInfoLayout.setContentsMargins(0, 20, 0, 0)

        # 用户头像
        avatarLabel = QLabel(self)
        avatarLabel.setProperty("class", "avatar")
        avatarPixmap = QPixmap('R-C.jpg')
        avatarLabel.setPixmap(avatarPixmap.scaled(150, 150, Qt.KeepAspectRatio))
        topInfoLayout.addWidget(avatarLabel)

        # 个人信息标签
        infoLabels = [
            ('姓名', QLineEdit, '常毅成'),
            ('学号', QLineEdit, '22354010'),
            ('专业', QLineEdit, '智能科学与技术')
        ]

        for label_text, widget_type, default_text in infoLabels:
            label = QLabel(label_text + ': ', self)
            label.setProperty("class", "info-label")
            if widget_type == QLineEdit:
                editText = QLineEdit(default_text)
                editText.setReadOnly(True)
                topInfoLayout.addWidget(label)
                topInfoLayout.addWidget(editText)
            else:
                topInfoLayout.addWidget(label)

        mainLayout.addLayout(topInfoLayout)

        # 中心内容区
        contentLayout = QGridLayout()
        contentLayout.setRowStretch(0, 1)
        contentLayout.setColumnStretch(0, 1)
        contentLayout.setContentsMargins(20, 20, 20, 20)

        # 文章发布区
        publishLayout = QHBoxLayout()
        self.titleEdit = QLineEdit(self)
        self.titleEdit.setPlaceholderText('请输入文章标题...')
        self.contentEdit = QTextEdit(self)
        self.contentEdit.setPlaceholderText('请输入文章内容...')

        publishButton = QPushButton('发布文章', self)
        publishButton.clicked.connect(self.publishArticle)

        publishLayout.addWidget(self.titleEdit)
        publishLayout.addWidget(self.contentEdit)
        publishLayout.addWidget(publishButton)
        contentLayout.addLayout(publishLayout, 0, 0)

        # 已发布文章区
        articlesLayout = QVBoxLayout()
        self.articlesList = QListWidget(self)
        self.articlesList.setSelectionMode(QListWidget.SingleSelection)
        articlesLayout.addWidget(self.articlesList)

        contentLayout.addLayout(articlesLayout, 0, 1)

        mainLayout.addLayout(contentLayout)

        # 底部控制区
        bottomLayout = QHBoxLayout()
        bottomLayout.setContentsMargins(0, 20, 0, 0)

        exitButton = QPushButton('退出系统', self)
        exitButton.clicked.connect(self.close)
        bottomLayout.addWidget(exitButton)

        mainLayout.addLayout(bottomLayout)  # 这里应该是 bottomLayout

    def publishArticle(self):
        # 获取文章标题和内容
        title = self.titleEdit.text()
        content = self.contentEdit.toPlainText()

        if not title or not content:
            QMessageBox.warning(self, '提示', '标题和内容不能为空!')
            return

        # 创建文章显示部件
        article_widget = QWidget()
        article_layout = QVBoxLayout(article_widget)
        article_layout.setContentsMargins(5, 5, 5, 5)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        content_label = QLabel(content)
        content_label.setWordWrap(True)  # 允许内容自动换行

        article_layout.addWidget(title_label)
        article_layout.addWidget(content_label)
        article_layout.addStretch()

        # 创建列表项并设置部件
        item = QListWidgetItem()
        item.setSizeHint(article_widget.sizeHint())  # 设置item的大小
        self.articlesList.addItem(item)
        self.articlesList.setItemWidget(item, article_widget)

        # 清空输入框
        self.titleEdit.clear()
        self.contentEdit.clear()

        # 设置当前选择项
        self.articlesList.setCurrentItem(item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PersonalBlog()
    ex.show()
    sys.exit(app.exec_())