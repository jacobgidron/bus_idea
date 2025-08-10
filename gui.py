import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QListWidget, QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit


import requests
import json

import map_from_bus_list


def get_bus_list_backend(term):
    res = requests.post("https://www.govmap.gov.il/api/search-service/autocomplete",
              data=json.dumps({"searchText": term,
              "language":"he",
              "filterType":"transportation",
              "isAccurate":True,
              "maxResults":100})
              ).json()
    res_dict = {}
    for i in res["results"]:
        ent = i["data"]
        key = f"{ent['agencyName']}-{ent['routeShortName']}: {ent['originCityName']}:{ent["originStationName"]}->{ent['destinationCityName']}:{ent["destinationStationName"]}"
        res_dict[key] = ent["routeId"]
    return res_dict



class ListSelectionExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("bus stop creator")
        # self.setGeometry(100, 100, 400, 300)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        self.layout = layout

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Enter your text here...")
        layout.addWidget(self.line_edit)


        self.line_num_button = QPushButton("Click me!")
        self.line_num_button.clicked.connect(self.get_bus_list)

        self.layout.addWidget(self.line_num_button)

        self.selected_label = QLabel("Selected Item: None")
        layout.addWidget(self.selected_label)
        self.list_widget = None



    def get_bus_list(self):

        entered_text = self.line_edit.text()
        self.line_desc_to_id =  get_bus_list_backend(entered_text.split()[0])
        print(entered_text.split()[0])
        if self.list_widget is None:
            self.list_widget = QListWidget()
            self.layout.addWidget(self.list_widget)
                    # Connect the itemSelectionChanged signal to a slot
            self.list_widget.itemSelectionChanged.connect(self.on_item_selection_changed)
        else:
            self.list_widget.clear()
        
        self.list_widget.addItems(self.line_desc_to_id.keys())


        self.button = QPushButton("make_csv")
        self.button.clicked.connect(self.make_csv)
        self.layout.addWidget(self.button)
    def make_csv(self):
        line_id = self.line_desc_to_id.get(self.selected_text)

        stops_info, line_info, line_ident = map_from_bus_list.bus_data_from_govmap_id(line_id)
        path = f"{self.selected_text.split(":")[0]}.csv"
        print(map_from_bus_list.write_buss_info_to_csv(stops_info, line_info,line_ident,line_id,path=path))


        
    def on_item_selection_changed(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            # Get the text of the first selected item (for single selection mode)
            selected_text = selected_items[0].text()
            self.selected_label.setText(f"Selected Item: {selected_text}")
            self.selected_text = selected_text
        else:
            self.selected_label.setText("Selected Item: None")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ListSelectionExample()
    window.show()
    sys.exit(app.exec())