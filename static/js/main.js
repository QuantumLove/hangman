(function () {

  'use strict';

  angular.module('HangmanApp', [])

  .controller('HangmanController', ['$scope', '$log', '$http', '$timeout',
    function($scope, $log, $http, $timeout) {

    $scope.score = 0;
    $scope.hangman = ["static/img/man0.png","static/img/man1.png","static/img/man2.png",
                      "static/img/man3.png","static/img/man4.png","static/img/man5.png"];
    $scope.lives = 5;

    $scope.startGame = function() {

      $log.log('Starting game');

      // Fire the API request
      $http.post('/start', {}).
        success(function(results) {
          $log.log(results);
        }).
        error(function(error) {
          $log.log(error);
        });

    };

    $scope.chooseLetter = function(letter) {

      $log.log('Choosing letter: ' + letter);

      // Fire the API request
      $http.post('/play', {letter: letter}).
        success(function(results) {
          $log.log(results);
        }).
        error(function(error) {
          $log.log(error);
        });

    };

    $scope.submitScore = function(name) {

      $log.log('Submitting name: ' + name);

      // Fire the API request
      $http.post('/end', {name: name}).
        success(function(results) {
          $log.log(results);
        }).
        error(function(error) {
          $log.log(error);
        });

    };


    $scope.highscores = function() {

      $log.log('Getting highscores');

      // Fire the API request
      $http.get('/highscores').
        success(function(results) {
          $log.log(results);
        }).
        error(function(error) {
          $log.log(error);
        });

    };

  }])


}());
