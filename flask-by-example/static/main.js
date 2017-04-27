(function () {
  'use strict';
  
  angular.module('WordcountApp', [])
  
  .controller('WordcountController', ['$scope', '$log', '$http', '$timeout',
    function($scope, $log, $http, $timeout) {
      $scope.submitButtonText = 'Submit';
      $scope.loading = false;
      $scope.urlerror = false;
      
      $scope.getResults = function() {
        var userInput = $scope.url;
        
        $http.post('/start', {"url": userInput}).success(function(results) {
          $log.log(results);
          getWordCount(results);
          $scope.wordcounts = null;
          $scope.loading = true;
          $scope.submitButtonText = 'Loading...';
        }).error(function(error) {
          $log.log(error);
        });
      };
      
      function getWordCount(jobID) {
        var timeout = "";
        var poller = function() {
          $http.get('/results/'+jobID).success(function(data, status, headers, config) {
            if(status === 202) {
              $log.log(data, status);
            } else if (status === 200) {
              $log.log(data);
              $scope.loading = false;
              $scope.submitButtonText = 'Submit';
              $scope.wordcounts = data;
              $timeout.cancel(timeout);
              return false;
            }
            timeout = $timeout(poller, 2000)
          }).error(function(error) {
            $log.log(error);
            $scope.loading = false;
            $scope.submitButtonText = 'Submit';
            $scope.urlerror = true;
          })
        };
        poller();
      }
    
    }
  ])
  
  .directive('wordCountChart', ['$parse', function($parse) {
    return {
      restrict: 'EA',
      replace: true,
      template: '<div id="chart"></div>',
      link: function(scope) {
        scope.$watch('wordcounts', function() {
          d3.select('#chart').selectAll('*').remove();
          var data = scope.wordcounts;
          for (var word in data) {
            console.log(">"+data[word][0])
            d3.select('#chart')
              .append('div')
              .style('width', function() {
                return (data[word][1] * 20) + 'px';
              })
              .text(function(d){
                return data[word][0];
              });
          }
        }, true);
      }
    };
  }]);
  
}());