import { inject } from "aurelia-framework";
import Api from "./utils/api";


@inject(Api)
export class App {
	page = 'customers';

	menu = [
		{key: 'customers', label: 'Clients'},
		{key: 'drivers', label: 'Drivers'},
		{key: 'zones', label: 'Zones'},
		{key: 'products', label: 'Produits'},
		{key: 'orders', label: 'Commandes'},
	]
	
	constructor(api){
		this.api = api;
	}
}
