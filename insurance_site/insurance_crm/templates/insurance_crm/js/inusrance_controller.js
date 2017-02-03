(function(){
    'use strict';
    angular.module('insurance_crm.demo', [])
        .controller('InsuranceCrmController', ['$scope', InsuranceCrmController]);

    function InsuranceCrmController($scope) {
        $scope.client = {
            name: 'Joe',
            status: 'bla'
        };
    }

}());