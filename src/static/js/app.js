function Trip(data) {
    this.title = data.title;
    this.city = data.city;
    this.price = data.price;
    this.start_date = data.start_date;
    this.end_date = data.end_date;
    this.people_min_count = data.people_min_count;
    this.main_photo = data.main_photo;
    this.photos = data.photos;
    this.absolute_url = data.absolute_url;
}

function TripListViewModel() {
    var self = this;

    self.min_people = ko.observable('');
    self.max_people = ko.observable('');

    self.trips = ko.observableArray([]);

    self.get_params = ko.computed(function() {
        return "?min_people=" + self.min_people() +
               "&max_people=" + self.max_people();
    }, this);

    ko.computed(function() {
        $.getJSON("/api/trips/" + self.get_params(), function(allData) {
            var mappedTasks = $.map(allData, function(item) { return new Trip(item) });
            self.trips(mappedTasks);
        });
    }).extend({ rateLimit: { timeout: 500, method: "notifyWhenChangesStop" } });
}

ko.applyBindings(new TripListViewModel());