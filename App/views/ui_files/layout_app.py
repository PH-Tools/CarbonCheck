# Form implementation generated from reading ui file './App/views/ui_files/layout_app.ui'
#
# Created by: PyQt6 UI code generator 6.5.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(757, 1005)
        self.container_body = QtWidgets.QWidget(parent=MainWindow)
        self.container_body.setObjectName("container_body")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.container_body)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.container_body)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_CreateBaseline = QtWidgets.QWidget()
        self.tab_CreateBaseline.setMaximumSize(QtCore.QSize(1157, 709))
        self.tab_CreateBaseline.setObjectName("tab_CreateBaseline")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_CreateBaseline)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.frame_baseline = QtWidgets.QFrame(parent=self.tab_CreateBaseline)
        self.frame_baseline.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame_baseline.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_baseline.setObjectName("frame_baseline")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_baseline)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.groupBox_baselinerTargetPHPP = QtWidgets.QGroupBox(parent=self.frame_baseline)
        self.groupBox_baselinerTargetPHPP.setObjectName("groupBox_baselinerTargetPHPP")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.groupBox_baselinerTargetPHPP)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_3 = QtWidgets.QLabel(parent=self.groupBox_baselinerTargetPHPP)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_8.addWidget(self.label_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lineEdit_selectSourcePHPPforBaseliner = QtWidgets.QLineEdit(parent=self.groupBox_baselinerTargetPHPP)
        self.lineEdit_selectSourcePHPPforBaseliner.setObjectName("lineEdit_selectSourcePHPPforBaseliner")
        self.horizontalLayout_4.addWidget(self.lineEdit_selectSourcePHPPforBaseliner)
        self.btn_selectSourcePHPPforBaseliner = QtWidgets.QPushButton(parent=self.groupBox_baselinerTargetPHPP)
        self.btn_selectSourcePHPPforBaseliner.setObjectName("btn_selectSourcePHPPforBaseliner")
        self.horizontalLayout_4.addWidget(self.btn_selectSourcePHPPforBaseliner)
        self.verticalLayout_8.addLayout(self.horizontalLayout_4)
        self.label_9 = QtWidgets.QLabel(parent=self.groupBox_baselinerTargetPHPP)
        self.label_9.setMinimumSize(QtCore.QSize(0, 50))
        self.label_9.setWordWrap(True)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_8.addWidget(self.label_9)
        self.verticalLayout_7.addWidget(self.groupBox_baselinerTargetPHPP)
        self.groupBox_baselinerOptions = QtWidgets.QGroupBox(parent=self.frame_baseline)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_baselinerOptions.sizePolicy().hasHeightForWidth())
        self.groupBox_baselinerOptions.setSizePolicy(sizePolicy)
        self.groupBox_baselinerOptions.setObjectName("groupBox_baselinerOptions")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.groupBox_baselinerOptions)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.frame_10 = QtWidgets.QFrame(parent=self.groupBox_baselinerOptions)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_10.setObjectName("frame_10")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frame_10)
        self.verticalLayout_10.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.frame_9 = QtWidgets.QFrame(parent=self.frame_10)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_9.setObjectName("frame_9")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.frame_9)
        self.horizontalLayout_12.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.comboBox_projBaselineCode = QtWidgets.QComboBox(parent=self.frame_9)
        self.comboBox_projBaselineCode.setObjectName("comboBox_projBaselineCode")
        self.horizontalLayout_12.addWidget(self.comboBox_projBaselineCode)
        self.label_11 = QtWidgets.QLabel(parent=self.frame_9)
        self.label_11.setMinimumSize(QtCore.QSize(200, 0))
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_12.addWidget(self.label_11)
        self.horizontalLayout_12.setStretch(0, 1)
        self.verticalLayout_10.addWidget(self.frame_9)
        self.frame_8 = QtWidgets.QFrame(parent=self.frame_10)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.frame_8)
        self.horizontalLayout_11.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.comboBox_projASHRAEClimateZone = QtWidgets.QComboBox(parent=self.frame_8)
        self.comboBox_projASHRAEClimateZone.setObjectName("comboBox_projASHRAEClimateZone")
        self.horizontalLayout_11.addWidget(self.comboBox_projASHRAEClimateZone)
        self.label_10 = QtWidgets.QLabel(parent=self.frame_8)
        self.label_10.setMinimumSize(QtCore.QSize(200, 0))
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_11.addWidget(self.label_10)
        self.horizontalLayout_11.setStretch(0, 1)
        self.verticalLayout_10.addWidget(self.frame_8)
        self.label_12 = QtWidgets.QLabel(parent=self.frame_10)
        self.label_12.setWordWrap(True)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_10.addWidget(self.label_12)
        self.verticalLayout_9.addWidget(self.frame_10)
        self.frame_2 = QtWidgets.QFrame(parent=self.groupBox_baselinerOptions)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_3.setContentsMargins(2, 6, 2, 6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.checkBox_baseliner_setSkylightAreas = QtWidgets.QCheckBox(parent=self.frame_2)
        self.checkBox_baseliner_setSkylightAreas.setMinimumSize(QtCore.QSize(250, 0))
        self.checkBox_baseliner_setSkylightAreas.setChecked(True)
        self.checkBox_baseliner_setSkylightAreas.setObjectName("checkBox_baseliner_setSkylightAreas")
        self.gridLayout_3.addWidget(self.checkBox_baseliner_setSkylightAreas, 3, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_8.setWordWrap(True)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 2, 2, 1, 1)
        self.checkBox_baseliner_setWindowUValues = QtWidgets.QCheckBox(parent=self.frame_2)
        self.checkBox_baseliner_setWindowUValues.setMinimumSize(QtCore.QSize(250, 0))
        self.checkBox_baseliner_setWindowUValues.setChecked(True)
        self.checkBox_baseliner_setWindowUValues.setObjectName("checkBox_baseliner_setWindowUValues")
        self.gridLayout_3.addWidget(self.checkBox_baseliner_setWindowUValues, 1, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_7.setWordWrap(True)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 3, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 4, 2, 1, 1)
        self.checkBox_baseliner_setSpaceLightingLPD = QtWidgets.QCheckBox(parent=self.frame_2)
        self.checkBox_baseliner_setSpaceLightingLPD.setMinimumSize(QtCore.QSize(250, 0))
        self.checkBox_baseliner_setSpaceLightingLPD.setChecked(True)
        self.checkBox_baseliner_setSpaceLightingLPD.setObjectName("checkBox_baseliner_setSpaceLightingLPD")
        self.gridLayout_3.addWidget(self.checkBox_baseliner_setSpaceLightingLPD, 4, 0, 1, 1)
        self.checkBox_baseliner_setEnvelopeUValues = QtWidgets.QCheckBox(parent=self.frame_2)
        self.checkBox_baseliner_setEnvelopeUValues.setMinimumSize(QtCore.QSize(250, 0))
        self.checkBox_baseliner_setEnvelopeUValues.setChecked(True)
        self.checkBox_baseliner_setEnvelopeUValues.setObjectName("checkBox_baseliner_setEnvelopeUValues")
        self.gridLayout_3.addWidget(self.checkBox_baseliner_setEnvelopeUValues, 0, 0, 1, 1)
        self.checkBox_baseliner_setWindowAreas = QtWidgets.QCheckBox(parent=self.frame_2)
        self.checkBox_baseliner_setWindowAreas.setMinimumSize(QtCore.QSize(250, 0))
        self.checkBox_baseliner_setWindowAreas.setChecked(True)
        self.checkBox_baseliner_setWindowAreas.setObjectName("checkBox_baseliner_setWindowAreas")
        self.gridLayout_3.addWidget(self.checkBox_baseliner_setWindowAreas, 2, 0, 1, 1)
        self.line = QtWidgets.QFrame(parent=self.frame_2)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_3.addWidget(self.line, 0, 1, 1, 1)
        self.line_2 = QtWidgets.QFrame(parent=self.frame_2)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_3.addWidget(self.line_2, 1, 1, 1, 1)
        self.line_3 = QtWidgets.QFrame(parent=self.frame_2)
        self.line_3.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout_3.addWidget(self.line_3, 2, 1, 1, 1)
        self.line_4 = QtWidgets.QFrame(parent=self.frame_2)
        self.line_4.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout_3.addWidget(self.line_4, 3, 1, 1, 1)
        self.line_5 = QtWidgets.QFrame(parent=self.frame_2)
        self.line_5.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridLayout_3.addWidget(self.line_5, 4, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(parent=self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QtCore.QSize(0, 0))
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 1, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 0, 2, 1, 1)
        self.gridLayout_3.setColumnStretch(2, 1)
        self.verticalLayout_9.addWidget(self.frame_2)
        self.verticalLayout_7.addWidget(self.groupBox_baselinerOptions)
        self.groupBox_baselinerRun = QtWidgets.QGroupBox(parent=self.frame_baseline)
        self.groupBox_baselinerRun.setObjectName("groupBox_baselinerRun")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.groupBox_baselinerRun)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.label_baselinerRunNote = QtWidgets.QLabel(parent=self.groupBox_baselinerRun)
        self.label_baselinerRunNote.setWordWrap(True)
        self.label_baselinerRunNote.setObjectName("label_baselinerRunNote")
        self.verticalLayout_13.addWidget(self.label_baselinerRunNote)
        self.btn_writeBaselinePHPP = QtWidgets.QPushButton(parent=self.groupBox_baselinerRun)
        self.btn_writeBaselinePHPP.setObjectName("btn_writeBaselinePHPP")
        self.verticalLayout_13.addWidget(self.btn_writeBaselinePHPP)
        self.verticalLayout_7.addWidget(self.groupBox_baselinerRun)
        self.verticalLayout_6.addWidget(self.frame_baseline)
        self.tabWidget.addTab(self.tab_CreateBaseline, "")
        self.tab_OutputReport = QtWidgets.QWidget()
        self.tab_OutputReport.setObjectName("tab_OutputReport")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_OutputReport)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.frame_main = QtWidgets.QFrame(parent=self.tab_OutputReport)
        self.frame_main.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame_main.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_main.setObjectName("frame_main")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_main)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_Proj_Info = QtWidgets.QGroupBox(parent=self.frame_main)
        self.groupBox_Proj_Info.setObjectName("groupBox_Proj_Info")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_Proj_Info)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame = QtWidgets.QFrame(parent=self.groupBox_Proj_Info)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.form_layout_project_info = QtWidgets.QFormLayout()
        self.form_layout_project_info.setObjectName("form_layout_project_info")
        self.projectNameLabel = QtWidgets.QLabel(parent=self.frame)
        self.projectNameLabel.setObjectName("projectNameLabel")
        self.form_layout_project_info.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.projectNameLabel)
        self.line_edit_project_name = QtWidgets.QLineEdit(parent=self.frame)
        self.line_edit_project_name.setMinimumSize(QtCore.QSize(200, 0))
        self.line_edit_project_name.setObjectName("line_edit_project_name")
        self.form_layout_project_info.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.line_edit_project_name)
        self.clientNameLabel = QtWidgets.QLabel(parent=self.frame)
        self.clientNameLabel.setObjectName("clientNameLabel")
        self.form_layout_project_info.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.clientNameLabel)
        self.line_edit_client_name = QtWidgets.QLineEdit(parent=self.frame)
        self.line_edit_client_name.setMinimumSize(QtCore.QSize(200, 0))
        self.line_edit_client_name.setObjectName("line_edit_client_name")
        self.form_layout_project_info.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.line_edit_client_name)
        self.gridLayout_2.addLayout(self.form_layout_project_info, 2, 0, 1, 1)
        self.tree_view_team_info = QtWidgets.QTreeView(parent=self.frame)
        self.tree_view_team_info.setUniformRowHeights(False)
        self.tree_view_team_info.setHeaderHidden(True)
        self.tree_view_team_info.setObjectName("tree_view_team_info")
        self.gridLayout_2.addWidget(self.tree_view_team_info, 2, 1, 1, 1)
        self.label_team_info = QtWidgets.QLabel(parent=self.frame)
        self.label_team_info.setObjectName("label_team_info")
        self.gridLayout_2.addWidget(self.label_team_info, 0, 1, 1, 1)
        self.lable_project_info = QtWidgets.QLabel(parent=self.frame)
        self.lable_project_info.setObjectName("lable_project_info")
        self.gridLayout_2.addWidget(self.lable_project_info, 0, 0, 1, 1)
        self.btn_add_team_info = QtWidgets.QPushButton(parent=self.frame)
        self.btn_add_team_info.setObjectName("btn_add_team_info")
        self.gridLayout_2.addWidget(self.btn_add_team_info, 3, 1, 1, 1)
        self.gridLayout_2.setColumnStretch(1, 1)
        self.verticalLayout_3.addWidget(self.frame)
        self.verticalLayout_2.addWidget(self.groupBox_Proj_Info)
        self.groupBox_Bldg_Data = QtWidgets.QGroupBox(parent=self.frame_main)
        self.groupBox_Bldg_Data.setObjectName("groupBox_Bldg_Data")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_Bldg_Data)
        self.gridLayout.setObjectName("gridLayout")
        self.tree_view_proposed = QtWidgets.QTreeView(parent=self.groupBox_Bldg_Data)
        self.tree_view_proposed.setObjectName("tree_view_proposed")
        self.gridLayout.addWidget(self.tree_view_proposed, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=self.groupBox_Bldg_Data)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(parent=self.groupBox_Bldg_Data)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.tree_view_baseline = QtWidgets.QTreeView(parent=self.groupBox_Bldg_Data)
        self.tree_view_baseline.setObjectName("tree_view_baseline")
        self.gridLayout.addWidget(self.tree_view_baseline, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMaximumSize)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_add_proposed_seg = QtWidgets.QPushButton(parent=self.groupBox_Bldg_Data)
        self.btn_add_proposed_seg.setObjectName("btn_add_proposed_seg")
        self.horizontalLayout_3.addWidget(self.btn_add_proposed_seg)
        self.btn_del_proposed_seg = QtWidgets.QPushButton(parent=self.groupBox_Bldg_Data)
        self.btn_del_proposed_seg.setObjectName("btn_del_proposed_seg")
        self.horizontalLayout_3.addWidget(self.btn_del_proposed_seg)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 1, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_add_baseline_seg = QtWidgets.QPushButton(parent=self.groupBox_Bldg_Data)
        self.btn_add_baseline_seg.setObjectName("btn_add_baseline_seg")
        self.horizontalLayout_2.addWidget(self.btn_add_baseline_seg)
        self.btn_del_baseline_seg = QtWidgets.QPushButton(parent=self.groupBox_Bldg_Data)
        self.btn_del_baseline_seg.setObjectName("btn_del_baseline_seg")
        self.horizontalLayout_2.addWidget(self.btn_del_baseline_seg)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_Bldg_Data)
        self.groupBox_Create_Report = QtWidgets.QGroupBox(parent=self.frame_main)
        self.groupBox_Create_Report.setObjectName("groupBox_Create_Report")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_Create_Report)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_create_report = QtWidgets.QFrame(parent=self.groupBox_Create_Report)
        self.frame_create_report.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame_create_report.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_create_report.setObjectName("frame_create_report")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_create_report)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.btn_create_report = QtWidgets.QPushButton(parent=self.frame_create_report)
        self.btn_create_report.setObjectName("btn_create_report")
        self.horizontalLayout_6.addWidget(self.btn_create_report)
        self.verticalLayout_4.addWidget(self.frame_create_report)
        self.verticalLayout_2.addWidget(self.groupBox_Create_Report)
        self.verticalLayout_5.addWidget(self.frame_main)
        self.tabWidget.addTab(self.tab_OutputReport, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.frame_output = QtWidgets.QFrame(parent=self.container_body)
        self.frame_output.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame_output.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_output.setObjectName("frame_output")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_output)
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textEdit_output = QtWidgets.QTextEdit(parent=self.frame_output)
        self.textEdit_output.setReadOnly(True)
        self.textEdit_output.setObjectName("textEdit_output")
        self.horizontalLayout.addWidget(self.textEdit_output)
        self.verticalLayout.addWidget(self.frame_output)
        MainWindow.setCentralWidget(self.container_body)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 757, 37))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(parent=MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtGui.QAction(parent=MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtGui.QAction(parent=MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionClose = QtGui.QAction(parent=MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionExport_Report_To = QtGui.QAction(parent=MainWindow)
        self.actionExport_Report_To.setObjectName("actionExport_Report_To")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExport_Report_To)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CarbonCheck"))
        self.groupBox_baselinerTargetPHPP.setTitle(_translate("MainWindow", "1. Baseline: Source PHPP"))
        self.label_3.setText(_translate("MainWindow", "Select the \'source\' PHPP file. The values of this file will be reset to the code-require \'baseline\' settings."))
        self.btn_selectSourcePHPPforBaseliner.setText(_translate("MainWindow", "Select Source..."))
        self.label_9.setText(_translate("MainWindow", "Specify the options for the baseline construction below. Baseline values will be automatically assigned to the inputs of the \'source\' file selected above based on the Climate Zone and Baseline Code selected."))
        self.groupBox_baselinerOptions.setTitle(_translate("MainWindow", "2. Baseline: Options"))
        self.label_11.setText(_translate("MainWindow", "Baseline Code"))
        self.label_10.setText(_translate("MainWindow", "ASHRAE Climate Zone"))
        self.label_12.setText(_translate("MainWindow", "<html><head/><body><p><a href=\"https://up.codes/viewer/new_york/ny-energy-conservation-code-2020/chapter/CE_2/ce-definitions#climate_zone\"><span style=\" text-decoration: underline; color:#0000ff;\">Climate zones</span></a> from <a href=\"https://up.codes/viewer/new_york/ny-energy-conservation-code-2020/chapter/CE_3/ce-general-requirements#table_C301.1\"><span style=\" text-decoration: underline; color:#0000ff;\">ECCNYS Table C301.1</span></a> shall be used for determining the baseline requirements.</p></body></html>"))
        self.checkBox_baseliner_setSkylightAreas.setText(_translate("MainWindow", "Set Skylight Areas"))
        self.label_8.setText(_translate("MainWindow", "If the total Window-wall-ratio is above the baseline limit, scale down the size of all window surfaces."))
        self.checkBox_baseliner_setWindowUValues.setText(_translate("MainWindow", "Set Window U-Values"))
        self.label_7.setText(_translate("MainWindow", "If the Skylight-to-roof ratio is above the baseline limit, scale down the size of all skylight surfaces."))
        self.label_6.setText(_translate("MainWindow", "Set the installed-power-density of all spaces to the baseline required values."))
        self.checkBox_baseliner_setSpaceLightingLPD.setText(_translate("MainWindow", "Set Space Lighting"))
        self.checkBox_baseliner_setEnvelopeUValues.setText(_translate("MainWindow", "Set Opaque Surface U-Values"))
        self.checkBox_baseliner_setWindowAreas.setText(_translate("MainWindow", "Set Window Areas"))
        self.label_5.setText(_translate("MainWindow", "Build new baseline glass and frames. Reset all window surface component assignments."))
        self.label_4.setText(_translate("MainWindow", "Build new baseline constructions for all opaque surfaces and reset the surfaces assembly assignments."))
        self.groupBox_baselinerRun.setTitle(_translate("MainWindow", "3. Baseline: Run"))
        self.label_baselinerRunNote.setText(_translate("MainWindow", "Click the button below to run the Baseline builder. This will modify the \'source\' PHPP file specified above and set the specified values in that file to the code-required baseline inputs. NOTE: Be sure that you have made copy of the source PHPP BEFORE running this baseline builder. "))
        self.btn_writeBaselinePHPP.setText(_translate("MainWindow", "Write Baseline PHPP"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_CreateBaseline), _translate("MainWindow", "Create Baseline PHPP"))
        self.groupBox_Proj_Info.setTitle(_translate("MainWindow", "1. Project Data"))
        self.projectNameLabel.setText(_translate("MainWindow", "Project Name:"))
        self.clientNameLabel.setText(_translate("MainWindow", "Client Name:"))
        self.label_team_info.setText(_translate("MainWindow", "Project Information"))
        self.lable_project_info.setText(_translate("MainWindow", "Project Information"))
        self.btn_add_team_info.setText(_translate("MainWindow", "Add Project Team / Site"))
        self.groupBox_Bldg_Data.setTitle(_translate("MainWindow", "2. Building Segment Data"))
        self.label_2.setText(_translate("MainWindow", "PROPOSED"))
        self.label.setText(_translate("MainWindow", "BASELINE"))
        self.btn_add_proposed_seg.setText(_translate("MainWindow", "Add Segment"))
        self.btn_del_proposed_seg.setText(_translate("MainWindow", "Remove Segment"))
        self.btn_add_baseline_seg.setText(_translate("MainWindow", "Add Segment"))
        self.btn_del_baseline_seg.setText(_translate("MainWindow", "Remove Segment"))
        self.groupBox_Create_Report.setTitle(_translate("MainWindow", "3. Create Report"))
        self.btn_create_report.setText(_translate("MainWindow", "Create Report"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_OutputReport), _translate("MainWindow", "Output Report"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open..."))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Save..."))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As..."))
        self.actionSave_As.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionClose.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actionExport_Report_To.setText(_translate("MainWindow", "Create Report..."))
