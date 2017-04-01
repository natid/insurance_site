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

        // if ( !vm.task )
        // {
        //     vm.task = {
        //         'id'                : '',
        //         'title'             : '',
        //         'notes'             : '',
        //         'startDate'         : new Date(),
        //         'startDateTimeStamp': new Date().getTime(),
        //         'dueDate'           : '',
        //         'dueDateTimeStamp'  : '',
        //         'completed'         : false,
        //         'starred'           : false,
        //         'important'         : false,
        //         'deleted'           : false,
        //         'tags'              : []
        //     };
        //     vm.title = 'New Task';
        //     vm.newTask = true;
        //     vm.task.tags = [];
        // }

        // // Methods
        // vm.addNewTask = addNewTask;
        // vm.saveTask = saveTask;
        // vm.deleteTask = deleteTask;
        // vm.newTag = newTag;
        vm.closeDialog = closeDialog;
        vm.addCustomer = addCustomer;

        // //////////

        // /**
        //  * Add new task
        //  */
        // function addNewTask()
        // {
        //     vm.tasks.unshift(vm.task);

        //     closeDialog();
        // }

        // /**
        //  * Save task
        //  */
        // function saveTask()
        // {
        //     // Dummy save action
        //     for ( var i = 0; i < vm.tasks.length; i++ )
        //     {
        //         if ( vm.tasks[i].id === vm.task.id )
        //         {
        //             vm.tasks[i] = angular.copy(vm.task);
        //             break;
        //         }
        //     }

        //     closeDialog();
        // }

        // /**
        //  * Delete task
        //  */
        // function deleteTask()
        // {
        //     var confirm = $mdDialog.confirm()
        //         .title('Are you sure?')
        //         .content('The Task will be deleted.')
        //         .ariaLabel('Delete Task')
        //         .ok('Delete')
        //         .cancel('Cancel')
        //         .targetEvent(event);

        //     $mdDialog.show(confirm).then(function ()
        //     {
        //         // Dummy delete action
        //         for ( var i = 0; i < vm.tasks.length; i++ )
        //         {
        //             if ( vm.tasks[i].id === vm.task.id )
        //             {
        //                 vm.tasks[i].deleted = true;
        //                 break;
        //             }
        //         }
        //     }, function ()
        //     {
        //         // Cancel Action
        //     });
        // }


        // /**
        //  * New tag
        //  *
        //  * @param chip
        //  * @returns {{label: *, color: string}}
        //  */
        // function newTag(chip)
        // {
        //     var tagColors = ['#388E3C', '#F44336', '#FF9800', '#0091EA', '#9C27B0'];

        //     return {
        //         name : chip,
        //         label: chip,
        //         color: tagColors[Math.floor(Math.random() * (tagColors.length))]
        //     };
        // }

        /**
         * Add New Customer
         */
        function addCustomer() {
            var agent_id = 1; // TODO USE REAL VALUE
            CustomersService.addCustomer(agent_id, vm.customer.id, vm.customer.name, vm.customer.phone, vm.customer.notes, vm.customer.status)
                .then(function(response){
                    customers.push(new CustomersService.Customers(vm.customer.id, vm.customer.name, vm.customer.phone, vm.customer.status, vm.customer.notes));
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