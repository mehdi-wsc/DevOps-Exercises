import { inject } from "aurelia-framework";
import Api from "../../utils/api";


@inject(Api)
export class ZoneList {
    list = [];
    
    constructor(api){
        this.api = api;
    }

    attached(){
        this.loadList();
    }

    loadList(){
        this.api.get("/zones")
            .then(r => this.list = r);
    }
}