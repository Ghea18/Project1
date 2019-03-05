class g2_ajax{ 
    constructor(form, link){
        this._method = 'POST';
        this._link = link;
        this._element = null;
        this._btn = null;
        this._color = '#FFFFFF';
        let parent = this;
        this._query ='';
        this._respons;
        this._tabReq;
        this._seriesReq
        var f_id;
        var f_val;
        if (form!=null) {
          if(typeof(form)==='string'){
            this._method = form;
          }else{
            form.addEventListener("click", function(event){
              event.preventDefault();
            });
            for (var i = 0; i < form.length; i++) {
                f_id  =  form.elements[i].id;
                f_val =  form.elements[i].value;
                if(f_id != null && f_id != '' && f_val != null && f_val != ''){
                    if(i>0){this._query += "&";}
                    this._query += f_id + "=" + f_val;
                }
            }
          }
        }
        /* The variable that makes Ajax possible! */
        try {
           /* Opera 8.0+, Firefox, Safari */
           this._ajax = new XMLHttpRequest();
        }catch (e) {
           /* Internet Explorer Browsers */
           try {
              this._ajax = new ActiveXObject("Msxml2.XMLHTTP");
           }catch (e) {
              try{
                 this._ajax = new ActiveXObject("Microsoft.XMLHTTP");
              }catch (e){
                 /* Something went wrong */
                 alert("Your browser broke!");
                 return false;
              }
           }
        }
    }
    getURL(data){
        if(Array.isArray(data)){
            for(i=0; i <= data.leght; i++){
                if(i==0){
                   this._query += data[i]+',';
                }else{
                   this._query += '&'+data[i]+',';
                }
            }
        }
        else{
           this._query = data;
        }
    }
    postURL(data, add){
        if(Array.isArray(data)){
           for(i=0; i <= data.leght; i++){
              if(i==0){
                 this._query += data[i]+',';
              }else{
                 this._query += '&'+data[i]+',';
              }
           }
        }
        else if(add){
           this._query = this._query + data;
        }else{
           this._query = data;
        }
    }
    BtnID(loc, color){
        if(loc != null){
           this._btn = loc;
        }
        if(color != '' && color != null){
           this._color = color;
        }
    }
    ToID(loc){
         if(loc != null && loc != null){
              this._element = loc;
         }else{
             console.log('ToID fail to set')
         }
    }
    method(method){
         if(method != null && method != null){
              this._method = method;
         }else{
             console.log('Method fail to set')
         }
    }
    form(form){
        var f_id;
        var f_val;
        for (var i = 0; i < form.length; i++) {
            f_id  =  form.elements[i].id;
            f_val =  form.elements[i].value;
            if(f_id != null && f_id != '' && f_val != null && f_val != ''){
                if(i>0){this._query += "&";}
                this._query += f_id + "=" + f_val;
            }
        }
    }
    table(bol){
        this._tabReq = bol;
    }
    series(bol){
        this._seriesReq = bol;
    }
    send(id, lod, color){
        if(lod != null && lod != ''){
           this._btn = lod;
        }
        if(color != '' && color != null){
           this._color = color;
        }
        if(id != null && id != ''){
              this._element = id;
        }

        var btn = this._btn;
        var element = this._element;
        var buildTab = this._tabReq;
        var buildSeries = this._seriesReq;
        var result;
        var notif = 0;
        var btnLast;
        if(this._method.toLowerCase()=='post'){
            console.log('do post ajax!');
            this._ajax.open(this._method, this._link, true);
            this._ajax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            console.log("Send: "+this._query);
            this._ajax.send(this._query);
        }else if(this._method.toLowerCase()=='get'){
            console.log('do get ajax!');
            console.log("Send: "+this._query);
            this._ajax.open(this._method, this._link + "?"+ this._query, true);
            this._ajax.send(null);
        }else{
            console.log('Method not set!')
        }
        
        addtoBTN('<div class="g2ajax-load-timer"></div> <style type="text/css"> /* Timer*/ .g2ajax-load-timer{color: '+this._color+'; width: 20px; height: 20px; background-color: transparent; box-shadow: inset 0px 0px 0px 2px '+this._color+'; border-radius: 50%; position: relative;} .g2ajax-load-timer:after, .g2ajax-load-timer:before{position: absolute; content:""; background-color: '+this._color+'; } .g2ajax-load-timer:after{width: 8px; height: 2px; top: 9px; left: 9px; -webkit-transform-origin: 1px 1px; -moz-transform-origin: 1px 1px; transform-origin: 1px 1px; -webkit-animation: minhand 2s linear infinite; -moz-animation: minhand 2s linear infinite; animation: minhand 2s linear infinite; } .g2ajax-load-timer:before{width: 7px; height: 2px; top: 9px; left: 9px; -webkit-transform-origin: 1px 1px; -moz-transform-origin: 1px 1px; transform-origin: 1px 1px; -webkit-animation: hrhand 8s linear infinite; -moz-animation: hrhand 8s linear infinite; animation: hrhand 8s linear infinite; } @-webkit-keyframes minhand{0%{-webkit-transform:rotate(0deg)} 100%{-webkit-transform:rotate(360deg)} } @-moz-keyframes minhand{0%{-moz-transform:rotate(0deg)} 100%{-moz-transform:rotate(360deg)} } @keyframes minhand{0%{transform:rotate(0deg)} 100%{transform:rotate(360deg)} } @-webkit-keyframes hrhand{0%{-webkit-transform:rotate(0deg)} 100%{-webkit-transform:rotate(360deg)} } @-moz-keyframes hrhand{0%{-moz-transform:rotate(0deg)} 100%{-moz-transform:rotate(360deg)} } @keyframes hrhand{0%{transform:rotate(0deg)} 100%{transform:rotate(360deg)} } </style>');

        this._ajax.onreadystatechange = function(){
            if(this.readyState == 4){
              if(this.status == 200){
                console.log('puting ajax in page!');
                if(addtoHTML(this.responseText)==false){
                    result = this.responseText;}
                else{
                    result = true;
                }
                addtoBTN(btnLast);
                console.log('ajax done!');
              } else if(this.status >= 500 ) {
                  // internal server error
                  addtoBTN(btnLast);
                  console.log('ajax failed! internal server error ('+this.status+')');
              } else if ( this.status >= 402 && this.status <= 420 ) {
                 // error
                  addtoBTN(btnLast);
                  console.log('ajax failed! something error ('+this.status+')');
              } else if( this.status == 400 || this.statuss == 401 ) {
                 // bad request & unauthorized error
                  addtoBTN(btnLast);
                  console.log('ajax failed! bad request & unauthorized error ('+this.status+')');
              }
           }
           if(this.readyState == 3){
              console.log('Waiting ajax response!');
           }
           if(this.readyState == 2){
              console.log('request ajax send!');
           }
        }
        const sleep = (milliseconds) => {
            return new Promise(resolve => setTimeout(resolve, milliseconds))
        }
        function addtoBTN(TEXT){
            if(btn != null && btn != ''){
                btnLast = btn.innerHTML;
                btn.innerHTML = TEXT;
            }
        }
        function addtoHTML(TEXT){
            if(element!=null && element!=''){
                if(buildTab == true){
                    var tabl = new g2_table();
                    var table = tabl.build(TEXT);
                    console.log(table);
                    document.getElementById(element).innerHTML = '';
                    document.getElementById(element).appendChild(table);
                }else if(buildSeries == true){
                    var json = JSON.parse(TEXT);
                    document.getElementById(element).innerHTML = '';
                    console.log('Add Series')
                    for (var e in json) {
                        sleep(1000);
                        try {
                            document.getElementById(element).appendChild(g2_response(json[e])); 
                        } catch (error) {
                            console.log(error)
                            document.getElementById(element).appendChild(json[e]);
                        }
                    };
                }
                else {
                    document.getElementById(element).innerHTML = TEXT;
                }
                return true;
            }else{
                if(notif==0){
                    notif=1;
                    console.log('ID HTML Element not set');
                    return false;
                }
            }
        }
        return result;
    }
}