(function ()
{
    'use strict';

    angular
        .module('app.customers')
        .service('CustomersService', CustomersService);
    
    var baseURL = 'http://127.0.0.1:8000';
    /** @ngInject */
    function CustomersService($q, $http)
    {
        function Customer(id, name, phone, status, notes){
            this.id = id;
            this.name = name;
            this.phone = phone;
            this.status = status;
            this.notes = notes;
        }

        function addCustomer(agent_id, id, name, phone, notes, status) {
            var d = $q.defer();
            var customer = {
                agent:agent_id,
                id_number:id,
                name:name,
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
                        cs.push(new Customer(customer.id_number, customer.name, customer.phone_number,customer.status));
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
                    d.resolve(new Customer(customer.id_number, customer.name, customer.phone_number,customer.status));
                }, function(response) {
                    d.reject(response);
                });
            return d.promise;
        }

        return {
            getCustomers:getCustomers,
            addCustomer:addCustomer,
            getCustomer:getCustomer
        }
    }
})();
