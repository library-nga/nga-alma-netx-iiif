// Primo VE custom IIIF viewer
//
// Uses the Primo PNX source record ID to construct the NGA Library IIIF
// manifest URL. The local display field lds01 controls whether the viewer
// is displayed for the record.

app.controller('imageViewerAfterController', [
    '$sce',
    '$scope',
    function ($sce, $scope) {
        var vm = this;

        vm.show = false;
        vm.manifest_link = '';

        var item = vm.parentCtrl.item;
        var pnx = item && item.pnx;

        if (!pnx || !pnx.control || !pnx.display) {
            return;
        }

        var sourceRecordId = pnx.control.sourcerecordid;
        var viewer = pnx.display.lds01;

        if (!sourceRecordId) {
            return;
        }

        // Primo PNX values may be arrays. Use the first value when needed.
        if (Array.isArray(sourceRecordId)) {
            sourceRecordId = sourceRecordId[0];
        }

        if (Array.isArray(viewer)) {
            viewer = viewer[0];
        }

        vm.manifest_link =
            'https://libraryimage.nga.gov/manifest/mms/' +
            sourceRecordId +
            '.json';

        $scope.manifest_trust_link = $sce.trustAsResourceUrl(
            'https://libraryimage.nga.gov/uv/?manifest=' +
            encodeURIComponent(vm.manifest_link)
        );

        vm.show = viewer === 'viewer';
    }
]);
