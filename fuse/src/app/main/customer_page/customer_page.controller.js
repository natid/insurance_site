(function ()
{
    'use strict';

    angular
        .module('app.customer_page')
        .controller('CustomerPageController', CustomerPageController);

    /** @ngInject */
    function CustomerPageController($document, $mdDialog, $state, CustomersService)
    {
        var vm = this;
        vm.chat = true;
        vm.customer = null
        var customerId = $state.params.id;
        vm.companiesData = {};

        CustomersService.getCustomer(customerId).then(function(customer){
            vm.customer = customer;
        }, function(error) {
             ////
            vm.customer = {
                "id": 2,
                "name": "Elisha",
                "notes": "",
                "status": null,
                "phone_number": "123345546",
                "id_number": "0",
                "agent": 2
            };
            ////
            console.warn(error);
        });

        CustomersService.getInsuranceCompanies(customerId).then(function(companies){
            vm.companies = companies;
        });

        vm.getCompanyData = function(companyId) {
            CustomersService.getCompanyData(customerId, companyId).then(function(response) {
                vm.companiesData[companyId] = response;
                console.log(vm.companiesData);
            })
        }
        // Data
        // Methods
      
        //////////
    }
})();
