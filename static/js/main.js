(function () {

    'use strict';

    angular.module('HangmanApp', ['ngMaterial'])

    .controller('HangmanController', ['$scope', '$log', '$http', '$timeout', '$mdDialog',
    function($scope, $log, $http, $timeout, $mdDialog) {

        $scope.start = function() {

            $scope.score = 0;
            $scope.lives = 6;
            $scope.category = '';
            $scope.spaces = {};
            $scope.hint = '';
            $scope.win = false;

            $scope.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
            'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];


            $scope.canvas();

            // Clear canvas
            $scope.context.clearRect(0, 0, 400, 400);
            $scope.drawFrame();

            $scope.startGame();

        };

        $scope.startGame = function() {

            // Fire the API request JSON.stringify(data)
            $http({
                url: '/start',
                method: "POST",
                headers: { 'Content-Type': 'application/json' },
                data: {}
                }).success(function(data) {
                    $scope.startLevel();
                }).error(function(error) {
                    $log.log('error: ' + error);
            });
        };

        $scope.startLevel = function() {
            $scope.win = false;
            $scope.hint = '';

            // Fire the API request
            $http({
                url: '/newLevel',
                method: "POST",
                headers: { 'Content-Type': 'application/json' },
                data: {}
                }).success(function(data) {
                    $scope.category = data.category;
                    $scope.spaces = Array.from({length: data.spaces}, (v, i) => '_');
                    $scope.resetChoices();
                }).error(function(error) {
                    $log.log('error: ' + error);
            });

        };

        $scope.chooseLetter = function(letter) {

            if($scope.lives <= 0 || $scope.win == true) return;

            var key = angular.element(document.querySelector('[value="' + letter + '"]'));

            // Todo: check if active in key.attr('class') to stop request

            key.attr("class", "active");

            // Fire the API request
            $http({
                url: '/play',
                method: "POST",
                headers: { 'Content-Type': 'application/json' },
                data: {letter: letter}
                }).success(function(data) {

                    $scope.score = data.score;

                    if (data.result == 'win' || data.result == 'correct') {
                        for (var i = 0; i < data.positions.length ; i++) {
                            $scope.spaces[data.positions[i]] = letter;
                        }
                    } else {
                        $scope.incorrectGuess();
                    }

                    if (data.result == 'win') {
                        // TODO: Do something cool when winning
                        $scope.win = true;
                    } else if (data.result == 'lost') {
                        $scope.promptName();
                    };

                }).error(function(error) {
                    $log.log('error: ' + error);
            });

        };


        $scope.getHint = function() {

            // Fire the API request
            $http({
                url: '/hint',
                method: "POST",
                headers: { 'Content-Type': 'application/json' },
                data: {}
                }).success(function(data) {
                    $log.log('...Got the hint!');
                    $scope.hint = data.hint;
                    $scope.score = data.score;
                }).error(function(error) {
                    $log.log('error: ' + error);
            });

        };

        $scope.promptName = function(event) {
            var confirm = $mdDialog.prompt()
                .title('You lost!')
                .textContent('Enter you name')
                .placeholder('Your name (max 20 characters)')
                .ariaLabel('name')
                .targetEvent(event)
                .ok('Submit')
                .cancel('No thanks');

            $mdDialog.show(confirm).then(function(result) {
                // Submit
                $scope.submitScore(result);
                $scope.highscores();
            }, function() {
                // Score not saved
                $scope.highscores();
            });



        };

        $scope.submitScore = function(name) {

            //TODO: Validate name size

            // Fire the API request
            $http({
                url: '/end',
                method: "POST",
                headers: { 'Content-Type': 'application/json' },
                data: {name: name}
                }).success(function(data) {

                }).error(function(error) {
                    $log.log('error: ' + error);
            });

        };

        $scope.highscores = function() {

            // Fire the API request
            $http({
                url: '/highscores',
                method: "GET"
                }).success(function(data) {
                    // Open scores
                    $scope.scores = data.scores;
                    $mdDialog.show({
                        //targetEvent: $event,
                        template:'static/partials/highscores.html',
                        scope: angular.extend($scope.$new(), { close: function() {$mdDialog.cancel();} })
                        //controller: 'GreetingController',
                        //onComplete: afterShowAnimation,
                        //locals: { employee: $scope.userName }
                    });

                }).error(function(error) {
                    $log.log('error: ' + error);
            });
        };



        // Auxiliary
        $scope.resetChoices = function() {
            for (var i = 0; i < $scope.alphabet.length ; i++) {
                var key = angular.element(document.querySelector('[value="' + $scope.alphabet[i] + '"]'));
                key.removeAttr("class", "active");
            }
        };

        $scope.incorrectGuess = function () {
            $scope.drawArray[--$scope.lives]();
        }


        // Hangman graphics
        $scope.canvas =  function(){
            var canvas = document.getElementById('hangman');
            $scope.context = canvas.getContext('2d');
            $scope.context.beginPath();
            $scope.context.strokeStyle = "#fff";
            $scope.context.lineWidth = 2;
        };

        var draw = function($pathFromx, $pathFromy, $pathTox, $pathToy) {

            // TODO: Make it animated
            $scope.context.moveTo($pathFromx, $pathFromy);
            $scope.context.lineTo($pathTox, $pathToy);
            $scope.context.stroke();
        }

        $scope.drawFrame = function() {
            draw (0, 150, 150, 150);
            draw (10, 0, 10, 600);
            draw (0, 5, 70, 5);
            draw (60, 5, 60, 15);
        };

        var head = function(){
            $scope.context.beginPath();
            $scope.context.arc(60, 25, 10, 0, Math.PI*2, true);
            $scope.context.stroke();
        }

        var torso = function() {
            draw (60, 36, 60, 70);
        };

        var rightArm = function() {
            draw (60, 46, 100, 50);
        };

        var leftArm = function() {
            draw (60, 46, 20, 50);
        };

        var rightLeg = function() {
            draw (60, 70, 100, 100);
        };

        var leftLeg = function() {
            draw (60, 70, 20, 100);
        };

        $scope.drawArray = [rightLeg, leftLeg, rightArm, leftArm,  torso,  head];

  }])


}());
