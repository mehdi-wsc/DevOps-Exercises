import { inject } from "aurelia-framework";
import Api from "../../utils/api";


@inject(Api)
export class ProductList {
    list = [];
    
    constructor(api){
        this.api = api;
    }

    attached(){
        this.loadList();
    }

    loadList(){
        this.api.get("/products")
            .then(r => this.list = r);
    }
}