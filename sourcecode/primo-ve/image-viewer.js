(function () {
    "use strict";

    var app = angular.module('viewCustom', ['angularLoad', 'googleAnalytics']);
    // var app = angular.module('viewCustom', ['angularLoad','nga-footer','nga-header']);

    // Beginning of viewer
    app.controller('imageViewerAfterController', [
        '$sce',
        '$scope',
        '$injector',
        function ($sce, $scope) {
            var vm = this;

            this.$onInit = function () {
                vm.gbs_sourcerecordid = [];
                vm.manifest_link = "";
                vm.availability = [];
                vm.viewer = [];
                vm.manifestlibrary = "mms";
                vm.iiifviewer = "uv";

                if ('sourceid' in vm.parentCtrl.item.pnx.control) {
                    vm.gbs_sourcerecordid = vm.parentCtrl.item.pnx.control.sourcerecordid;
                    vm.viewer = vm.parentCtrl.item.pnx.display.lds01;
                }

                if (vm.parentCtrl.item.delivery.bestlocation.libraryCode == "IMAGES") {
                    vm.manifestlibrary = "ic";
                    vm.iiifviewer = "mirador";
                }

                vm.manifest_link =
                    "https://libraryimage.nga.gov/manifest/" +
                    vm.manifestlibrary +
                    "/" +
                    vm.gbs_sourcerecordid +
                    ".json";

                $scope.manifest_trust_link = $sce.trustAsResourceUrl(
                    "https://libraryimage.nga.gov/" +
                    vm.iiifviewer +
                    "/?manifest=" +
                    vm.manifest_link
                );

                $scope.manifest_short_link = $sce.trustAsResourceUrl(
                    "https://libraryimage.nga.gov/" +
                    vm.iiifviewer +
                    "/?manifest=" +
                    vm.manifest_link +
                    "&showinfo=no"
                );

                vm.show = false;
                vm.show_digital = false;

                if (vm.viewer == "viewer") {
                    vm.show = true;

                    if (vm.parentCtrl.item.delivery.deliveryCategory.includes("Alma-D")) {
                        vm.show_digital = true;
                        vm.show = false;
                    }
                }
            };
        }
    ]);

    /*
     * Temporarily show viewer under Details for titles without a digital
     * representation in place yet; remove after migration is complete.
     */
    app.component("prmActionListAfter", {
        bindings: {
            parentCtrl: '<'
        },
        controller: 'imageViewerAfterController',
        template: '\n       <br> <div class="image-preview" ng-if="$ctrl.show" flex-md="100" flex-lg="100" flex-xl="100" flex>\n            <div class="">\n                <div layout="row" layout-align="center center" class="layout-align-center-center layout-row">\n                    <h4 class="section-title md-title light-text">Image View</h4>\n                    <a href="{{manifest_trust_link}}"><img src="https://libraryimage.nga.gov/manifest/iiif-logo.png" alt="IIIF icon" height="30"></a>\n                    <md-divider flex></md-divider>\n                </div>\n                <div class="">\n                    <div class="spaced-rows">\n                        <div style="padding-top:1em;">\n                            <div class="imageWrapper">\n                                <iframe ng-src="{{manifest_short_link}}" allowfullscreen frameborder="0"></iframe>\n                            </div>\n                        </div>\n                    </div>\n                </div>\n            </div>\n        </div>'
    });

    app.component("prmAlmaViewitAfter", {
        bindings: {
            parentCtrl: '<'
        },
        controller: 'imageViewerAfterController',
        template: '\n       <div class="image-preview" ng-if="$ctrl.show_digital" flex-md="100" flex-lg="100" flex-xl="100" flex>\n            <div class="">\n                <div layout="row" layout-align="center center" class="layout-align-center-center layout-row"></div>\n                <div class="">\n                    <div class="spaced-rows">\n                        <div style="padding-top:1em;">\n                            <div class="imageWrapper">\n                                <iframe ng-src="{{manifest_short_link}}" allowfullscreen frameborder="0"></iframe>\n                            </div>\n                        </div>\n                    </div>\n                </div>\n            </div>\n        </div>'
    });
    // End of viewer
}());
