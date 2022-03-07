  var editor = grapesjs.init({
    clearOnRender: true,
    height: '100%',
    storageManager: {
      id: '#html',             // Prefix identifier that will be used inside storing and loading
      type: 'local',          // Type of the storage
      autosave: true,         // Store data automatically
      autoload: true,         // Autoload stored data on init
      stepsBeforeSave: 1,     // If autosave enabled, indicates how many changes are necessary before store method is triggered
      storeHtml: true,        // Enable/Disable storing of components as HTML string
    },
    assetManager: {
      assets: null,
      upload: 0,
      uploadText: 'Uploading is not available in this demo',
        },
    container : '#editor',
    fromElement: true,
    plugins: ['gjs-preset-newsletter', 'gjs-plugin-ckeditor', 'gjs-blocks-basic'],
    pluginsOpts: {
      'gjs-preset-newsletter': {
        modalLabelImport: 'Paste all your code here below and click import',
        modalLabelExport: 'Copy the code and use it wherever you want',
        codeViewerTheme: 'material',
        //defaultTemplate: templateImport,
        importPlaceholder: '<table class="table"><tr><td class="cell">Hello world!</td></tr></table>',
        cellStyle: {
          'font-size': '12px',
          'font-weight': 300,
          'vertical-align': 'top',
          color: 'rgb(111, 119, 125)',
          margin: 0,
          padding: 0,
        }
      },
      'gjs-plugin-ckeditor': {
        position: 'center',
            options: {
              startupFocus: true,
              extraAllowedContent: '*(*);*{*}', // Allows any class and any inline style
              allowedContent: true, // Disable auto-formatting, class removing, etc.
              enterMode: CKEDITOR.ENTER_BR,
              extraPlugins: 'sharedspace,justify,colorbutton,panelbutton,font',
              toolbar: [
                { name: 'styles', items: ['Font', 'FontSize' ] },
                ['Bold', 'Italic', 'Underline', 'Strike'],
                {name: 'paragraph', items : [ 'NumberedList', 'BulletedList']},
                {name: 'links', items: ['Link', 'Unlink']},
                {name: 'colors', items: [ 'TextColor', 'BGColor' ]},
          ],
        }
      },
      'gjs-blocks-basic': {
         blocks:['video', 'map'],
        }
    }
  });



        var form = document.querySelector('form');
        form.onsubmit = function() {
          // Populate hidden form on submit
          var html = document.querySelector('input[name=html]');
          html.value = editor.runCommand('gjs-get-inlined-html');
          console.log("Submitted", $(form).serialize(), $(form).serializeArray());
          }