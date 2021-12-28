import { HttpClient } from 'aurelia-fetch-client';


var ieFormData = function ieFormData(){
    if(window.FormData == undefined)
    {
        this.processData = true;
        this.contentType = 'application/x-www-form-urlencoded';
        this.append = function(name, value) {
            this[name] = value == undefined ? "" : value;
            return true;
        }
    }
    else
    {
        var formdata = new FormData();
        formdata.processData = false;
        formdata.contentType = false;
        return formdata;
    }
}

export class ApiError extends Error {
    status  = 0;
    subcode = "";
    message = "";
    details = "";
    data    = {};

    constructor(e){
        super(e);

        if(typeof e === "string")
            this.subcode = e;
        else {
            const { status, message, subcode, details, ...data } = e;
            this.status = status;
            this.message = message;
            this.subcode = subcode;
            this.details = details;
            this.data = data;
        }
    }
}


/**
 * Class used to handle API calls
 */
export default class Api{
    constructor(){
        this.url = process.env.API_URL;
        this.headers = {};
        this.webStorage = window.localStorage || window.sessionStorage;
        this.log_errors = false;
        this.client = new HttpClient();
        this.cookies = true;
    }

    enableCookies() {
        this.cookies = true;
    }

    /**
     * Will add headers to instance
     *
     * @param {*} data
     */
    addHeaders(data = {}){
        for(let h in data){
            if (data.hasOwnProperty(h))
                this.headers[h] = data[h];
        }
    }

    /**
     * Will replace instance's headers
     * @param {*} data
     */
    setHeaders(data = null){
        this.headers = data;
    }

    getFetchParams(method, data, opt={}){
        // Base header construction
        let _headers = new Headers(this.headers);

		/**
		 * Retrieving csrf headers
		 */
		let csrf_token = this.webStorage.getItem("csrf_token");

		if(csrf_token)
			_headers.set("X-Csrf-Token", csrf_token);

        // Request options, method, headers and body if needed
        let options = {
            method: method,
            headers: _headers
        };

        if(opt.redirect)
            options.redirect = opt.redirect;

        if (this.cookies)
            options.credentials = "include";

        /*
         * Creating body if needed
         */
        if(data !== null){
            let formData = new ieFormData();
            Object.keys(data).forEach(key => {
                let value = data[key]
                if (Array.isArray(value)) {
                    value.forEach(subValue => formData.append(key + "[]", subValue))
                } else {
                    formData.append(key, value)
                }
            });
            options.body = formData;
        }

        return options;
    }

    /**
     *
     * @param {string} method POST, GET, PUT, DELETE
     * @param {string} endpoint
     * @param {*} data POST data if needed empty for no body
     */
    _fetch(method, endpoint, data=null, opt={}){
        let options = this.getFetchParams(method, data, opt);

        let response_type = 'json';
        if(opt.response_type)
            response_type = opt.response_type;

        /**
         * Main call
         */
        return this.client.fetch(this.url + endpoint, options)
            .then(res => {
                if(!res.ok || (res.status !== 200 && res.status !== 201))
                    return res.json().then(e => {throw new ApiError(e);});
                    
                if(response_type === 'json')
                    return res.json();
                else if(response_type === 'blob')
                    return res.blob();
            })
            .then( res => { return Promise.resolve(res); })
            .catch(e => {
                if(this.log_errors)
                    console.log(e);
                throw e;
            });
    }

    get(endpoint, response_type='json', options={}){
        return this._fetch("GET", endpoint, null, Object.assign(options, {response_type: response_type}));
    }

    del(endpoint, data){
        return this._fetch("DELETE", endpoint, data);
    }

    post(endpoint, data, options={}){
        return this._fetch("POST", endpoint, data, options);
    }

    put(endpoint, data){
        return this._fetch("PUT", endpoint, data);
    }

    download(endpoint, filename, data=null, option={}){
        let method = "GET";
        if(option.method)
            method = option.method;

        return this._fetch(method, endpoint, data, {
            response_type: 'blob'
        })
            .then(blob => {
                let url = window.URL.createObjectURL(blob);
                let a = document.createElement('a');
                a.href = url;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                setTimeout(() => {
                    document.body.removeChild(a);
                    window.URL.revokeObjectURL(url);  
                }, 100);                     
            })
            .catch(e => {
                throw e;
            });
    }

    async getDataUri(blob, callback) {
        return await new Promise((resolve, reject) => {
            let reader = new FileReader();
            reader.readAsDataURL(blob);
            reader.onload = () => {
                resolve(reader.result);
            };
        });
    }    

    async getFile(file_key, asURI=false){
        let options = this.getFetchParams("GET", null);

        let data = await this.client.fetch(this.url + "/files/" + file_key, options);
        if(data.status !== 200)
            throw Error();
            
        let blob = await data.blob();

        if(asURI)
            return this.getDataUri(blob);
        else 
            return window.URL.createObjectURL(blob);
    }
}
