(function(){
    'use strict';
    angular.module('insurance_crm.demo', [])
        .controller('ClientController', ['$scope', '$http', '$location', ClientController]);

    function ClientController($scope, $http, $location) {
        $scope.client = [];

        (function() {
                var url = $location.absUrl().split('/')
                var id = url[url.length-1]
                $http.get('/insurance_crm/clients/'+id+'/').then(function(response){
                $scope.client = response.data;
            });
        }());
    }

}());