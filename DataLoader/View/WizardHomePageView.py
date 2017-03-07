import wx


class WizardHomePageView(wx.Panel):
    def __init__(self, parent):
        super(WizardHomePageView, self).__init__(parent)

        # Create components
        instructions_text = wx.StaticText(self, label="Load YODA file or Excel Template")
        # self.input_file_text_ctrl = RichTextCtrl(self)
        self.input_file_text_ctrl = wx.TextCtrl(self)
        self.browse_button = wx.Button(self, label="Browse")
        yoda_check_box = wx.CheckBox(self, label="YODA")
        excel_check_box = wx.CheckBox(self, label="Excel Template")
        odm2_check_box = wx.CheckBox(self, label="ODM2 Database")

        # Style components
        self.input_file_text_ctrl.SetHint("Input file...")

        # Sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        static_box_sizer = wx.StaticBoxSizer(wx.StaticBox(self, label="Export to"), orient=wx.VERTICAL)

        # Add components to sizer
        input_sizer.Add(self.input_file_text_ctrl, 1, wx.EXPAND | wx.ALL, 2)
        input_sizer.Add(self.browse_button, 0, wx.ALL, 0)
        static_box_sizer.Add(yoda_check_box, 0, flag=wx.EXPAND | wx.ALL, border=15)
        static_box_sizer.Add(excel_check_box, 0, flag=wx.EXPAND | wx.ALL, border=15)
        static_box_sizer.Add(odm2_check_box, 0, flag=wx.EXPAND | wx.ALL, border=15)

        sizer.Add(instructions_text, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(input_sizer, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(static_box_sizer, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)
        self.Hide()

        # Bindings
        self.browse_button.Bind(wx.EVT_BUTTON, self.on_browse_button)

    def on_browse_button(self, event):
        pass