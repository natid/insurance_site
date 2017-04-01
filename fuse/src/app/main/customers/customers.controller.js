(function ()
{
    'use strict';

    angular
        .module('app.customers')
        .controller('CustomersController', CustomersController);

    /** @ngInject */
    function CustomersController($document, $mdDialog, CustomersService)
    {
        var vm = this;

        // Data
        CustomersService.getCustomers().then(function(customers){
            vm.customers = customers;
        })
        // Methods
        vm.addCustomer = function(ev) {
            $mdDialog.show({
                controller         : 'TaskDialogController',
                controllerAs       : 'vm',
                templateUrl        : 'app/main/apps/todo/dialogs/task/task-dialog.html',
                parent             : angular.element($document.body),
                targetEvent        : ev,
                clickOutsideToClose: true,
                locals             : {
                    //Tasks: vm.tasks,
                    event: ev
                }
            });
        }
        //////////
    }
})();
