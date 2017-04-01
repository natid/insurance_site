(function ()
{
    'use strict';

    angular
        .module('app.customers')
        .service('CustomersService', CustomersService);

    /** @ngInject */
    function CustomersService($q, $http)
    {
        function Customer(name, email, phone, status){
            this.name = name;
            this.email = email;
            this.phone = phone;
            this.status = status;
        }

        function getCustomers() {
            var d = $q.defer();
            $http({
                    method: 'GET',
                    url: 'http://127.0.0.1:8000/insurance_crm/clients/',
                    xhrFields: {
                        withCredentials: true
                    },
                    crossDomain: true,
                    headers:{"Authorization":"Basic ZEBnbWFpbC5jb206MTIz"}
                }).then(function(response){
                    var cs = [];
                    for (var i =0 ; i< response.data.length; ++i) {
                        var customer = response.data[i];
                        cs.push(new Customer(customer.name, customer.email, customer.phone_number,customer.status));
                    }
                    d.resolve(cs)
                }, function(response) {
                    d.reject(response);
                });
            return d.promise;
        }
        return {
            getCustomers:getCustomers
        }
    }
})();
