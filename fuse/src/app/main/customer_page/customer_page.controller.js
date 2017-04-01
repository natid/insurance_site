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
        CustomersService.getCustomer($state.params.id).then(function(customer){
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
        CustomersService.getInsuranceCompanies().then(function(companies){
            vm.companies = companies;
        });

        // Data
        // Methods
      
        //////////
    }
})();
