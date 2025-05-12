import Alpine from 'alpinejs';
import { Message } from './message';
import { BraintreeForm } from "./braintree"

Alpine.data('message', Message);
Alpine.data("braintree_form", BraintreeForm)

Alpine.start();
