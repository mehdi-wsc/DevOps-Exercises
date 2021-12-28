import { inject } from "aurelia-framework";
import Api from "../../utils/api";


@inject(Api)
export class CustomerList {
    list = [];
    
    constructor(api){
        this.api = api;
    }

    attached(){
        this.loadList();
    }

    loadList(){
        this.api.get("/customers")
            .then(r => this.list = r);
    }
}