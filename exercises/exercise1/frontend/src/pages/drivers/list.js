import { inject } from "aurelia-framework";
import Api from "../../utils/api";


@inject(Api)
export class DriverList {
    list = [];
    zones = {};
    
    constructor(api){
        this.api = api;
    }

    attached(){
        this.loadList();
    }

    loadList(){
        this.api.get("/zones")
            .then(res => {
                let zones = {};
                res.forEach(z => {
                    zones[z.id] = z;
                });
                this.zones = zones;
                this.api.get("/drivers")
                    .then(r => this.list = r);
            });
    }

    getZone
}