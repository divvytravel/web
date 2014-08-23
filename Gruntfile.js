module.exports = function(grunt) {

  grunt.initConfig({
    sass: {
      dist: {
        files: {
          'src/static/css/theme.css': 'src/frontend/styles/theme.scss'
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-sass');

  grunt.registerTask('default', ['sass']);
};