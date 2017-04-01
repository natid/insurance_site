(function ()
{
    'use strict';

    angular
        .module('app.customers')
        .controller('CustomersController', CustomersController);

    /** @ngInject */
    function CustomersController($state, $document, $mdDialog, CustomersService)
    {
        var vm = this;

        // Data
        CustomersService.getCustomers().then(function(customers){
            vm.customers = customers;
        })
        // Methods
        vm.addCustomer = function(ev) {
            $mdDialog.show({
                controller         : 'AddCustomerController',
                controllerAs       : 'vm',
                templateUrl        : 'app/main/customers/dialogs/add/add-customer-dialog.html',
                parent             : angular.element($document.body),
                targetEvent        : ev,
                clickOutsideToClose: true,
                locals             : {
                    customers: vm.customers,
                    event: ev
                }
            });
        }

        
        vm.showCustomer = function(id) {
            $state.go('app.customer_page', {id:id});
        }
        //////////
    }
})();
