(function ()
{
    'use strict';

    angular
        .module('app.customers')
        .service('CustomersService', CustomersService);
    //for production
    // var baseURL = 'https://poly-wizz.co.il';
   var baseURL = '';
    // var baseURL = 'http://localhost:8000'
    /** @ngInject */
    function CustomersService($q, $http)
    {
        function Customer(id, id_number, first_name, last_name, phone, status, notes){
            this.id = id;
            this.id_number = id_number;
            this.first_name = first_name;
            this.last_name = last_name;
            this.phone = phone;
            this.status = status;
            this.notes = notes;
        }

        function addCustomer(agent_id, id_number, first_name, last_name, phone, notes, status) {
            var d = $q.defer();
            var customer = {
                agent:agent_id,
                id_number:id_number,
                first_name:first_name,
                last_name:last_name,
                phone_number:phone,
                notes:notes,
                status:status
            }
            $http({
                    method: 'POST',
                    url: baseURL+'/insurance_crm/clients/',
                    data:customer
                }).then(function(response){
                    d.resolve(response)
                }, function(response) {
                    d.reject(response);
                });
            return d.promise;
        }

        function getCustomers() {
            var d = $q.defer();
            $http({
                    method: 'GET',
                    url: baseURL+'/insurance_crm/clients/',
                }).then(function(response){
                    var cs = [];
                    for (var i =0 ; i< response.data.length; ++i) {
                        var customer = response.data[i];
                        cs.push(new Customer(customer.id, customer.id_number, customer.first_name, customer.last_name, customer.phone_number,customer.status));
                    }
                    d.resolve(cs)
                }, function(response) {
                    d.reject(response);
                });
            return d.promise;
        }

        function getCustomer(id) {
            var d = $q.defer();
            $http({
                    method: 'GET',
                    url: baseURL+'/insurance_crm/clients/'+id
                }).then(function(response) {
                    var customer = response.data;
                    d.resolve(new Customer(id, customer.id_number, customer.first_name, customer.last_name, customer.phone_number,customer.status));
                }, function(response) {
                    d.reject(response);
                });
            return d.promise;
        }
        console.log($http)

        function getInsuranceCompanies(clientId) {
             var d = $q.defer();
            $http({
                    method: 'GET',
                    url: baseURL+'/insurance_crm/insurance_company_list?client_id='+clientId
                }).then(function(response) {
                    d.resolve(response.data);
                }, function(response) {
                    d.reject(response);
                });
            return d.promise;
        }

         function getCompanyData(clientId, companyId) {
             var d = $q.defer();
            // $http({
            //         method: 'GET',
            //         url: baseURL+'/insurance_crm/clients/'+id
            //     }).then(function(response) {
            //         var customer = response.data;
            //         d.resolve(new Customer(customer.id_number, customer.name, customer.phone_number,customer.status));
            //     }, function(response) {
            //         d.reject(response);
            //     });
            d.resolve([
               {data:"מייל תוכן"},
               {data:"גנן גידל דגן בגן"}
            ])
            return d.promise;
        }

        function sendToCellosign(customerId) {
            $http.get(baseURL+'/insurance_crm/cellosign?id='+customerId);
        }

        return {
            Customer:Customer,
            getCustomers:getCustomers,
            addCustomer:addCustomer,
            getCustomer:getCustomer,
            getInsuranceCompanies:getInsuranceCompanies,
            getCompanyData:getCompanyData,
            sendToCellosign:sendToCellosign
        }
    }
})();
