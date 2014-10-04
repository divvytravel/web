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

    self.city = ko.observable('');
    self.min_price = ko.observable('');
    self.max_price = ko.observable('');
    self.min_people = ko.observable('');
    self.max_people = ko.observable('');
    self.current_user = ko.observable('');
    self.current_tag = ko.observable('');

    self.trips = ko.observableArray([]);
    self.users = ko.observableArray([]);
    self.tags = ko.observableArray([]);

    self.get_params = ko.computed(function() {
        return "?city=" + self.city() +
               "&min_price=" + self.min_price() +
               "&max_price=" + self.max_price() +
               "&min_people=" + self.min_people() +
               "&max_people=" + self.max_people() +
               "&tag=" + self.current_tag();
    }, this);

    self.changeTag = function(tag) {
      if(self.current_tag() == tag.id){
          self.current_tag('');
      } else {
          self.current_tag(tag.id);
      };
    };

    ko.computed(function() {
        $.getJSON("/api/trips_users/" + self.get_params(), function(allData) {
            var mappedTasks = $.map(allData.trips, function(item) { return new Trip(item) });
            self.trips(mappedTasks);

            var mappedUsers = $.map(allData.users, function(item) { return new User(item) });
            self.users(mappedUsers);

            var mappedTags = $.map(allData.tags, function(item) { return new Tag(item) });
            self.tags(mappedTags);

            var old_current_tag = self.current_tag(),
                there_is_tag = false;

            for (var i = 0; i < self.tags().length; i++) {
              console.log(self.tags()[i]);

              if(self.tags()[i].id == old_current_tag){
                there_is_tag = true;
              }
            };
            console.log(there_is_tag);
        });
    }).extend({ rateLimit: { timeout: 500, method: "notifyWhenChangesStop" } });
}

ko.applyBindings(new TripListViewModel());