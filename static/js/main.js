(function () {

    'use strict';

    angular.module('HangmanApp', [])

    .controller('HangmanController', ['$scope', '$log', '$http', '$timeout',
    function($scope, $log, $http, $timeout) {

        $scope.score = 0;
        $scope.hangman = ["static/img/man0.png","static/img/man1.png","static/img/man2.png",
                  "static/img/man3.png","static/img/man4.png","static/img/man5.png"];
        $scope.lives = 6;

        $scope.startGame = function() {

            $log.log('Starting game');

            // Fire the API request JSON.stringify(data)
            $http({
                url: '/start',
                method: "POST",
                headers: { 'Content-Type': 'application/json' },
                data: {}
                }).success(function(data) {
                    console.log(data)
                    $scope.startLevel()
                }).error(function(error) {
                    $log.log(error);
            });
        };

        $scope.startLevel = function() {

            $log.log('Starting Level');

            // TODO: CleanUp letters and the rest

            // Fire the API request
            $http.post('/newLevel', {}).
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

            //TODO: Validate name size

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

        $scope.start = function() {

            $log.log('Starting Application');

            var alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
            'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
            't', 'u', 'v', 'w', 'x', 'y', 'z'];

            // Create alphabet ul
            var buttons = function () {
                myButtons = document.getElementById('buttons');
                letters = document.createElement('ul');

                for (var i = 0; i < alphabet.length; i++) {
                    letters.id = 'alphabet';
                    list = document.createElement('li');
                    list.id = 'letter';
                    list.innerHTML = alphabet[i];
                    check();
                    myButtons.appendChild(letters);
                    letters.appendChild(list);
                }
            }

            $scope.startGame();

        };

  }])


}());
