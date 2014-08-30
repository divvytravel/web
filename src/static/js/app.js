function Trip(data) {
    this.title = data.title;
    this.start_date = data.start_date;
    this.end_date = data.end_date;
}

function TripListViewModel() {
    var self = this;

    self.trips = ko.observableArray([]);

    self.updateTrips = function() {
        $.getJSON("/api/trips/", function(allData) {
            var mappedTasks = $.map(allData, function(item) { return new Trip(item) });
            self.trips(mappedTasks);
        });
    };
}

ko.applyBindings(new TripListViewModel());