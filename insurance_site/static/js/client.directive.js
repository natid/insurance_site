(function () {
    'use strict';

    angular.module('insurance_crm.demo')
        .directive('crmClient', ClientDirective);

    function ClientDirective() {
        return {
            templateUrl: '/static/html/client.html',
            restrict: 'E',
            controller: ['$scope', '$http', function ($scope, $http) {
                var url = '/insurance_crm/clients/' + $scope.client.id + '/';
                $scope.update = function () {
                    $http.put(
                        url,
                        $scope.client
                    );
                };

                $scope.delete = function () {
                    $http.delete(url).then(
                        function() {
                            var clients = $scope.agent.clients;
                            clients.splice(
                                clients.indexOf($scope.client),
                                1
                            );
                        }
                    );
                };

                $scope.modelOptions = {
                    debounce: 500
                };
            }]
        };
    }
})();