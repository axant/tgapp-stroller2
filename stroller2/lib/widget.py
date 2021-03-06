from stroller2.lib.ractive import RactiveWidget
from tw2.core import Param


class AjaxManagePhotos(RactiveWidget):
    action = Param('Url used to save newly uploaded photos', request_local=False)
    delete_action = Param('Url used to delete uploaded photos', request_local=False)
    permit_upload = Param('Whenever to enable upoad of new photos or only replace existing', request_local=False,
                          default=True)
    ractive_params = ['action', 'delete_action', 'permit_upload', 'css_class', 'id']

    ractive_template = '''
<div id="{{id}}" class="{{css_class ? css_class : ''}}">
    {{#photos}}
    <div class="photo" intro="fade">
        {{#delete_action}}
        <div class="photo-delete" on-tap="request_delete">&#10799;</div>
        {{/delete_action}}
        <div class="photo-picture photo-for-edit" data-photo-uid="{{uid}}" on-tap="request_upload">
            <img src="{{url}}" data-image-url="{{full_url}}"/>
        </div>
        <div class="photo-picture photo-for-modal" data-photo-uid="{{uid}}">
            <img src="{{url}}" data-image-url="{{full_url}}"/>
        </div>
        {{#loading}}
            <div class='loading-photo-div'></div>
        {{/loading}}
    </div>
    {{/photos}}
    {{#permit_upload}}
    <div class="photo-upload btn btn-primary" on-tap="request_upload" style="margin: 12px 0 0 10px;">carica foto</div>
    {{/permit_upload}}
</div>
'''

    ractive_init = '''
function(options) {
    if (this._super !== undefined) this._super(options);

    this.on({
      request_delete: function(click_evt) {
        var self = this;
        var xhr = new XMLHttpRequest();
        var data = new FormData();
        data.append('uid', click_evt.context.uid);
        xhr.open('DELETE', self.get('delete_action'), true);
        xhr.setRequestHeader("Cache-Control", "no-cache");
        xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");

        xhr.onload = function() {
            var result = JSON.parse(this.responseText);
            self.set('photos', result.photos);
        }

        xhr.send(data);
      },
      request_upload: function(click_evt) {

        var self = this;
        var filefield = document.createElement('input');
        filefield.type = "file";
        filefield.name = "picture";
        filefield.style = "display: none;"
        filefield.onchange = function() {
            var data = new FormData();
            data.append('file', filefield.files[0]);

            if (click_evt.context.uid)
                data.append('uid', click_evt.context.uid);

            var xhr = new XMLHttpRequest();
            xhr.open('POST', self.get('action'), true);
            xhr.setRequestHeader("Cache-Control", "no-cache");
            xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");

            xhr.onload = function() {
                var result = JSON.parse(this.responseText);
                self.set('photos', result.photos);
                self.set('loading', false);
            }

            self.set('loading', true);

            if (data.fake) {
               xhr.setRequestHeader("Content-Type", "multipart/form-data; boundary="+ data.boundary);
               xhr.sendAsBinary(data.toString());
            } else {
               xhr.send(data);
            }
        };

        window.document.body.appendChild(filefield);
        filefield.click();
        window.document.body.removeChild(filefield);

        $(".photo-for-modal").on("click", function() {
            $('#imagepreview').attr('src', $(this).find("img").attr('data-image-url')); // here asign the image to the modal when the user click the enlarge link
            $('#imagemodal').modal('show'); // imagemodal is the id attribute assigned to the bootstrap modal, then i use the show function
        });
      }
    });
}'''


