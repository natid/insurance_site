(function ()
{
    'use strict';

    angular
        .module('fuse')
        .controller('LoginController', LoginController)
        .directive('loginInput',loginInput);
    
    
    function loginInput($timeout) {
        return {
            restrict: 'A',
            // transclude: true,
            // scope: true,
            link: function(scope, elem, attr) { 
                var inputE = elem.find('input');
                var label = elem.find('label');
                
                inputE.on('keyup blur focus', function (e) {
                    if (e.type === 'keyup') {
                            if (inputE.val() === '') {
                        label.removeClass('active highlight');
                        } else {
                        label.addClass('active highlight');
                        }
                    } else if (e.type === 'blur') {
                        if( inputE.val() === '' ) {
                            label.removeClass('active highlight'); 
                            } else {
                            label.removeClass('highlight');   
                            }   
                    } else if (e.type === 'focus') {
                    
                    if( inputE.val() === '' ) {
                            label.removeClass('highlight'); 
                            } 
                    else if( inputE.val() !== '' ) {
                            label.addClass('highlight');
                            }
                    }

                });
            }
        };
    }

    /** @ngInject */
    function LoginController($rootScope,$location, AuthenticationService)
    {
        var vm = this;
        vm.loginState = 'login';
        $rootScope.$broadcast('msSplashScreen::remove');
        // Methods

        vm.login = function() {
            vm.dataLoading = true;
            AuthenticationService.Login(vm.username, vm.password)
                .then(function(response){
                    AuthenticationService.SetCredentials(vm.username, vm.password);
                    $location.path('/customers');
                },function(response) {
                    vm.message = "Failed";
                });
        };

        //////////
    }
})();
