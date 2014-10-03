function Trip(data) {
    this.title = data.title;
    this.city = data.city;
    this.price = data.price;
    this.start_date = data.start_date;
    this.end_date = data.end_date;
    this.period = data.period;
    this.people_min_count = data.people_min_count;
    this.main_photo = data.main_photo;
    this.photos = data.photos;
    this.peoples = data.peoples;
    this.absolute_url = data.absolute_url;
    this.tags = data.tags;
}

function User(data) {
    this.id = data.id;
    this.username = data.username;
    this.avatar_url = data.avatar_url;
}

function Tag(data) {
    this.id = data.id;
    this.name = data.name;
    this.slug = data.slug;
}

function TripListViewModel() {
    var self = this;

    self.min_people = ko.observable('');
    self.max_people = ko.observable('');
    self.current_user = ko.observable('');
    self.current_tag = ko.observable('');

    self.trips = ko.observableArray([]);
    self.users = ko.observableArray([]);
    self.tags = ko.observableArray([]);

    self.get_params = ko.computed(function() {
        return "?min_people=" + self.min_people() +
               "&max_people=" + self.max_people() +
               "&tag=" + self.current_tag();
    }, this);

    self.changeTag = function(tag) {
      self.current_tag(tag.id);
    };

    ko.computed(function() {
        $.getJSON("/api/trips_users/" + self.get_params(), function(allData) {
            var mappedTasks = $.map(allData.trips, function(item) { return new Trip(item) });
            self.trips(mappedTasks);

            var mappedUsers = $.map(allData.users, function(item) { return new User(item) });
            self.users(mappedUsers);

            var mappedTags = $.map(allData.tags, function(item) { return new Tag(item) });
            self.tags(mappedTags);
        });
    }).extend({ rateLimit: { timeout: 500, method: "notifyWhenChangesStop" } });
}

ko.applyBindings(new TripListViewModel());