from DataLoader.View.WizardView import WizardView
from WizardHomePageController import WizardHomePageController
from WizardYodaPageController import WizardYodaPageController
from WizardExcelPageController import WizardExcelPageController
from WizardDatabasePageController import WizardDatabasePageController
from WizardSummaryPageController import WizardSummaryPageController


class WizardController(WizardView):
    def __init__(self, parent):
        super(WizardController, self).__init__(parent)

        self.home_page = WizardHomePageController(self.body_panel, title="Yoda Wizard")
        self.yoda_page = WizardYodaPageController(self.body_panel, title="Yoda")
        self.excel_page = WizardExcelPageController(self.body_panel, title="Excel")
        self.database_page = WizardDatabasePageController(self.body_panel, title="OMD2")
        self.summary_page = WizardSummaryPageController(self. body_panel, title="Summary")

        self.add_page(self.home_page)
        self.add_page(self.yoda_page)
        self.add_page(self.excel_page)
        self.add_page(self.database_page)
        self.add_page(self.summary_page)

        self.show_home_page()
        # self.frame_sizer.Fit(self)
        self.SetSize((450, 450))

    def on_next_button(self, event):
        self.wizard_pages[self.page_number].Hide()

        # Boundary checking
        self.page_number = min(self.page_number + 1, len(self.wizard_pages) - 1)

        self.__update_page()

    def on_back_button(self, event):
        self.wizard_pages[self.page_number].Hide()

        # Boundary checking
        self.page_number = max(self.page_number - 1, 0)

        self.__update_page()

    def __update_page(self):
        self.title_text.SetLabel(self.wizard_pages[self.page_number].title)

        if self.page_number == 0:
            self.will_flip_to_first_page()
        elif self.page_number == len(self.wizard_pages) - 1:
            self.will_flip_to_last_page()
        else:
            self.next_button.SetLabel("Next")
            self.back_button.Show()

        self.wizard_pages[self.page_number].Show()
        self.body_panel.Layout()
        self.footer_panel.Layout()

    def will_flip_to_first_page(self):
        self.back_button.Hide()

    def will_flip_to_last_page(self):
        self.next_button.SetLabel("Finish")

    def show_home_page(self):
        for page in self.wizard_pages:
            page.Hide()

        self.page_number = 0
        self.__update_page()

