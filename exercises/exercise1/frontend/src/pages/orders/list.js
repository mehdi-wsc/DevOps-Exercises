import { inject } from "aurelia-framework";
import Api from "../../utils/api";


@inject(Api)
export class OrderList {
    list = [];
    
    constructor(api){
        this.api = api;
    }

    attached(){
        this.loadList();
    }

    loadList(){
        this.api.get("/deliveries")
            .then(r => this.list = r);
    }
}