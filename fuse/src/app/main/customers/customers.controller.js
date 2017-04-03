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
        vm.loadingProgress = true;
        // Data
        CustomersService.getCustomers().then(function(customers){
            vm.customers = customers;
        },function(response){
            console.warn(response);
        }).finally(function(){
            vm.loadingProgress = false;
        });
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
            }).then(function(){
                 CustomersService.getCustomers().then(function(customers){
                    vm.customers = customers;
                });
            });
        }

        
        vm.showCustomer = function(id) {
            $state.go('app.customer_page', {id:id});
        }
        //////////
    }
})();
