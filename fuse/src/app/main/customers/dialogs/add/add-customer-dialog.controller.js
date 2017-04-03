(function ()
{
    'use strict';

    angular
        .module('app.customers')
        .controller('AddCustomerController', AddCustomerController);

    /** @ngInject */
    function AddCustomerController($mdDialog, event, customers, CustomersService)
    {
        var vm = this;

        // // Data
        // vm.title = 'Edit Task';
        // vm.task = angular.copy(Task);
        // vm.tasks = Tasks;
        vm.newCustomer = true;
        vm.customer = null;
        vm.closeDialog = closeDialog;
        vm.addCustomer = addCustomer;


        /**
         * Add New Customer
         */
        function addCustomer() {
            var agent_id = 1; // TODO USE REAL VALUE
            CustomersService.addCustomer(agent_id, vm.customer.id, vm.customer.first_name, vm.customer.last_name, vm.customer.phone, vm.customer.notes, vm.customer.status)
                .then(function(response){
                    customers.push(new CustomersService.Customer(vm.customer.id, vm.customer.first_name, vm.customer.last_name, vm.customer.phone, vm.customer.status, vm.customer.notes));
                },function(response){
                    console.warn(response);
                });
            closeDialog();
        }

        /**
         * Close dialog
         */
        function closeDialog()
        {
            $mdDialog.hide();
        }
    }
})();