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
        vm.currentMailData = null;

        CustomersService.getCustomer(customerId).then(function(customer){
            vm.customer = customer;
        }, function(error) {
            console.warn(error);
        });

        CustomersService.getInsuranceCompanies(customerId).then(function(companies){
            vm.companies = companies;
        });

        vm.getCompanyData = function(companyId) {
            CustomersService.getCompanyData(customerId, companyId).then(function(response) {
                vm.companiesData[companyId] = response;                
            })
        }

        vm.sendToCellosign = function(customerId) {
            CustomersService.sendToCellosign(customerId);
        }

        vm.downlodFile = function(filename, data) {
            var element = document.createElement('a');
            element.setAttribute('href', 'data:text/plain;base64,' + encodeURIComponent(data));
            element.setAttribute('download', filename);

            element.style.display = 'none';
            document.body.appendChild(element);

            element.click();

            document.body.removeChild(element);
        }
        // Data
        // Methods
      
        //////////
    }
})();
