<?php

declare(strict_types=1);

namespace App\Application\Actions\User;

class UserInput {
    private $name;

    public function __construct($name) {
        $this->name = $name;
    }

    public function getName() {
        return $this->name;
    }
}