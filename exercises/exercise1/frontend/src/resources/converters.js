
import numeral from 'numeral';
import moment from "moment";


function formatNumber(value){
	return numeral(value).format('0.00');
}

function formatUtcDate(dateStr, format="dddd DD/MM/YY HH:mm"){
	let date = dateStr;
	if(!moment.isMoment(date))
		date = new Date(date);
	return moment(date).format(format);
}

export class FloorValueConverter {
	toView(value){
		return Math.floor(value);
	}
}

export class NumberFormatValueConverter {
	toView(value) {
		return formatNumber(value);
	}
}

export class NumberAddValueConverter {
	toView(value, addition) {
		let v = parseFloat(value) + parseFloat(addition);
		return formatNumber(v);
	}
}

export class HourSplitValueConverter {
	toView(value) {
		if (value)
		return (value.split(':')[0]);
	}
}

export class MinSplitValueConverter {
	toView(value) {
		if (value)
		return (value.split(':')[1]);
	}
}

export class TwoDigitsValueConverter{
	toView(value){
		if(typeof value === "string")
		value = parseFloat(value);
		if(0 <= value && value < 10) return "0" + value.toString();
		if(-10 < value && value < 0) return "-0" + (-1*value).toString();
		return value.toString();
	}
}

export class FileSizeValueConverter {
	toView(value){
		let unit = ['b', 'kb', 'Mb', 'Gb', 'Tb', 'Pb', 'Eb', 'Zb', 'Yb'];
		let radix = 1000;
		let bytes = Math.abs(value);
		let loop = 0;
		
		// calculate
		while (bytes >= radix) {
			bytes /= radix;
			++loop;
		}
		
		return `${bytes.toFixed(2)} ${unit[loop]}`;
	}
}

export class DateFormatValueConverter {
	toView(value, format) {
		if(!format)
		format = "ddd DD/MM/YY - HH:mm";
		return formatUtcDate(value, format);
	}
}