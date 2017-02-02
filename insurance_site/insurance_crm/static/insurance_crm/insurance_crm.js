(function(){
    'use strict';
    angular.module('insurance_crm.demo', [])
        .controller('InsuranceCrmController', ['$scope', '$http', InsuranceCrmController]);

    function InsuranceCrmController($scope, $http) {
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
        $scope.data = []

        $http.get('/insurance_crm/agents/').then(function(response){
            $scope.data = response.data;
        });

    }

}());