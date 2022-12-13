# Algumas gems
require "base64"
require "dotenv"
require "json"
require "net/http"
require "ruby-progressbar"
require "uri"

Dotenv.load

# Informações de autenticação
basic_auth_string = ENV['API_USERNAME'] + ':'
$base64_data = Base64.strict_encode64(basic_auth_string).to_str

# Caminho até o arquivo com os dados formatados
path = 'data/data.txt'
# Abrindo o arquivo
file = File.open(path)
# JSON com os dados dos sites
data = JSON.parse(file.read)
# Fechando o arquivo
file.close

total = data.length
# Barra de progresso
progressbar = ProgressBar.create({total: total})

# Função para realizar as requisições
def do_request(method, url_, body=nil)
  url = URI(url_)

  https = Net::HTTP.new(url.host, url.port)
  https.use_ssl = true

  case method
  when 'get'
    request = Net::HTTP::Get.new(url)
  when 'post'
    request = Net::HTTP::Post.new(url)
    request["Content-Type"] = "application/vnd.api+json"
    request.body = body
  end

  request["Authorization"] = "Basic " + $base64_data
  response = https.request(request)
  response
end

# Iniciar um teste
def start_test(url)
  body = JSON.dump({
    "data": {
      "type": "test",
      "attributes": {
        "url": url,
        "report": "legacy"
      }
    }
  })

  puts "\n> The test has already been requested!"

  do_request("post", 
             "https://gtmetrix.com/api/2.0/tests",
             body)  
end

# Gerar o relatório do teste
def get_report(url, filename)
  print "Waiting for the report"

  loop do 
    response = do_request('get', url)
    $body = JSON.parse(response.read_body)
    sleep(5)
    print "."
    
    begin
      state = $body["data"]["attributes"]["state"]
    rescue NoMethodError
      puts "Error requesting report for: #{filename}"
      break
    end

    break if !(state == "started" || state == "queued")
  end

  # Getting a report
  url = $body["data"]["links"]["report"]
  response = do_request('get', url + "/resources/report.pdf")

  system("clear")

  # Saving the report
  file = File.open("reports/#{filename}.pdf", "w")
  file.write(response.read_body)
  file.close
end

# Realizando os pedidos de teste e relatório
for site_data in data
  progressbar.increment
  puts "\nIt's the turn of the: #{site_data["name"]}"
  puts "#{progressbar.progress} out of #{total}"

  response = start_test(site_data["url"])
  body = JSON.parse(response.read_body)
  url = body["links"]["self"]

  filename = site_data["name"].downcase
  get_report(url, filename)
end
