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
        });

        // Data
        // Methods
      
        //////////
    }
})();
