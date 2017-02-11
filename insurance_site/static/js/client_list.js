(function(){
    'use strict';
    angular.module('insurance_crm.demo', [])
        .controller('ClientController', ['$scope', '$http', ClientController]);

    function ClientController($scope, $http) {
        $scope.data = []

        $http.get('/insurance_crm/clients/'+id).then(function(response){
            $scope.data = response.data;
        });

    }

}());