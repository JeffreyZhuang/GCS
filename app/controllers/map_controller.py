class MapController:
    def __init__(self, view, config_model, telemetry_model):
        self.view = view
        self.config_model = config_model
        self.telemetry_model = telemetry_model
        self.telemetry_model.data_changed.connect(self.update_flight_data)
        self.config_model.waypoints_updated.connect(self.update_waypoints)
        self.view.clicked.connect(self.map_clicked)
    
    def update_waypoints(self, waypoints):
        self.view.set_waypoints(waypoints)
        self.view.render()

    def update_flight_data(self, data):
        self.view.set_map_position(data["latest_packet"].data.gnss_latitude, 
                                   data["latest_packet"].data.gnss_longitude)
        self.view.set_plane_position(data["latest_packet"].data.gnss_latitude, 
                                     data["latest_packet"].data.gnss_longitude, 
                                     data["latest_packet"].data.heading)
        self.view.render()
    
    def map_clicked(self, pos):
        self.config_model.map_clicked(pos)