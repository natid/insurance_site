(function(){
    'use strict';
    angular.module('insurance_crm.demo', ['ngRoute'])
        .controller('InsuranceCrmController', ['$scope', '$http', 'Login', InsuranceCrmController]);

    function InsuranceCrmController($scope, $http, Login) {
        $scope.add = function (agent, client_name) {
            var n_client = {
                agent: agent.id,
                name: client_name
            };
            $http.post('/insurance_crm/clients/', n_client)
                .then(function(response) {
                    agent.clients.push(response.data)
                },
                function(){
                    alert('could not create client');
                });
        };


        Login.redirectIfNotLoggedIn();
        $scope.logout = Login.logout;

        $scope.data = []
        $http.get('/insurance_crm/agents/').then(function(response){
            $scope.data = response.data;
        });

    }

}());