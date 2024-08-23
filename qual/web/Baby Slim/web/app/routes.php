<?php

declare(strict_types=1);

use App\Application\Actions\User\ListUsersAction;
use App\Application\Actions\User\ViewUserAction;
use App\Application\Actions\User\UserInput;
use App\Application\Handlers\WAF;
use Psr\Http\Message\ResponseInterface as Response;
use Psr\Http\Message\ServerRequestInterface as Request;
use Slim\App;
use Slim\Interfaces\RouteCollectorProxyInterface as Group;


return function (App $app) {
    $app->options('/{routes:.*}', function (Request $request, Response $response) {
        // CORS Pre-Flight OPTIONS Request Handler
        return $response;
    });

    $app->get('/', function (Request $request, Response $response) {
        // $response->getBody()->write('Hello world!');
        $data = array('path' => 'echo', 'param' => 'name');
        $payload = json_encode($data);

        $response->getBody()->write($payload);
        return $response
                ->withHeader('Content-Type', 'application/json');

    });

    $app->get('/echo', function ($request, $response, $exception) {
        $name = $request->getQueryParams()["name"] ?? '';
        
        if (!util($name)['waf']->checkInput(util($name)['userInput']->getName())) {
            $serializedUserInput = serialize(util($name)['userInput']);
            $unserializedUserInput = unserialize($serializedUserInput);
            
            if ($unserializedUserInput instanceof UserInput) {
                $output = shell_exec("echo {$unserializedUserInput->getName()}");
                $data = json_encode(array('status' => 'success','msg' => $output));
                $response->getBody()->write($data);
                // $response->getBody()->write("<pre>$serializedUserInput</pre>");
            } else {
                $response->getBody()->write("Error unserializing object");
            }
        } else {
            $data = array('status' => 'failed', 'response' => $name);
            $payload = json_encode($data);

            $response->getBody()->write($payload);
        }
    
        return $response;
    });

    $app->group('/users', function (Group $group) {
        $group->get('', ListUsersAction::class);
        $group->get('/{id}', ViewUserAction::class);
    });
};















function util($name){
    $waf = new WAF();
    $userInput = new UserInput($name);

    // Mengembalikan dua variabel dalam bentuk array
    return array('waf' => $waf, 'userInput' => $userInput);
}