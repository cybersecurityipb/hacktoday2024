<?php

declare(strict_types=1);

namespace App\Application\Handlers;

class WAF {
    public function checkInput($input) {
        if (preg_match("/([^a-z])+/s", $input)) {
            return true;
        } else {
            return false;
        }
    }
}

$waf = new WAF();