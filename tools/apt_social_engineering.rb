#!/usr/bin/env ruby

# APT Social Engineering Toolkit
# Advanced social engineering analysis and simulation
# For educational and authorized penetration testing only

require 'json'
require 'date'

class APTSocialEngineering
  def initialize
    @results = {
      timestamp: Time.now.iso8601,
      target_analysis: {},
      email_analysis: {},
      psychological_profiling: {},
      recommendations: []
    }
  end

  def print_banner
    banner = <<~BANNER
      
        ___  _____ _____   _____           _       _____                      _             
       / _ \\|  _  |  __ \\ /  ___|         | |     /  ___|                    | |            
      / /_\\ \\ | | | |  \\/ \\ `--.  ___  ___| | __ \\ `--.  ___  __ _ _ __ ___| |_ ___ _ __ 
      |  _  | | | | | __   \\`--. \\/ _ \\/ __| |/ /  \\`--. \\/ _ \\/ _` | '__/ __| __/ _ \\ '__|
      | | | \\ \\_/ / |_\\ \\/\\__/ /  __/ (__|   <   /\\__/ /  __/ (_| | | | (__| ||  __/ |   
      \\_| |_/\\___/ \\____/ \\____/ \\___|\\___|_|\\_\\ \\____/ \\___|\\__,_|_|  \\___|\\__\\___|_|   

                          Social Engineering Toolkit
                     For Educational and Authorized Testing Only
    BANNER
    puts banner
  end

  def analyze_email_pattern(email)
    analysis = {
      email: email,
      domain: email.split('@').last,
      username: email.split('@').first,
      pattern_type: 'unknown',
      confidence: 0.0
    }

    patterns = {
      'first.last' => /^[a-z]+\\.[a-z]+$/i,
      'first_last' => /^[a-z]+_[a-z]+$/i,
      'firstlast' => /^[a-z][a-z]+[a-z]$/i,
      'flast' => /^[a-z][a-z]+$/i
    }

    username = analysis[:username]
    
    patterns.each do |pattern_name, regex|
      if username.match?(regex)
        analysis[:pattern_type] = pattern_name
        analysis[:confidence] = 0.8
        break
      end
    end

    analysis[:confidence] = [analysis[:confidence], 1.0].min
    analysis
  end

  def generate_email_variations(base_email)
    username, domain = base_email.split('@')
    variations = []

    variations << "#{username}@#{domain}"
    variations << "#{username.downcase}@#{domain}"
    
    if username.include?('.')
      parts = username.split('.')
      if parts.length == 2
        first, last = parts
        variations << "#{first}_#{last}@#{domain}"
        variations << "#{first[0]}#{last}@#{domain}"
        variations << "#{first}#{last}@#{domain}"
      end
    end

    variations.uniq
  end

  def psychological_profiling(name, email, company = nil)
    profile = {
      communication_style: 'unknown',
      likely_technical_level: 'unknown',
      organizational_role: 'unknown',
      risk_assessment: 'medium'
    }

    email_analysis = analyze_email_pattern(email)
    
    case email_analysis[:pattern_type]
    when 'first.last', 'first_last'
      profile[:communication_style] = 'formal'
    when 'firstlast', 'flast'
      profile[:communication_style] = 'practical'
    end

    technical_domains = ['github.com', 'gitlab.com']
    if technical_domains.include?(email_analysis[:domain])
      profile[:likely_technical_level] = 'high'
    else
      profile[:likely_technical_level] = 'variable'
    end

    if company
      profile[:organizational_role] = infer_role_from_email(email, company)
    end

    profile
  end

  def infer_role_from_email(email, company)
    username = email.split('@').first.downcase
    
    role_patterns = {
      'admin' => 'Administrator',
      'support' => 'Support Staff',
      'sales' => 'Sales',
      'marketing' => 'Marketing',
      'hr' => 'Human Resources',
      'it' => 'IT Staff',
      'dev' => 'Developer',
      'eng' => 'Engineer'
    }

    role_patterns.each do |pattern, role|
      return role if username.include?(pattern)
    end

    'General Staff'
  end

  def generate_spear_phishing_templates(target_info)
    templates = {
      urgent: {
        subject: "URGENT: Security Update Required - #{Date.today.strftime('%B %Y')}",
        body: "Dear #{target_info[:name] || 'Valued Employee'},\n\nOur security team has identified a critical vulnerability that requires immediate attention. Please review the attached security patch.\n\nBest regards,\nSecurity Team"
      },
      collaboration: {
        subject: "Follow-up: Project Discussion",
        body: "Hello #{target_info[:name] || 'Colleague'},\n\nI wanted to follow up on our recent discussion. Could you please review the attached document?\n\nLooking forward to your thoughts,\nProject Team"
      }
    }

    templates
  end

  def analyze_target(target_info)
    puts "[*] Analyzing target: #{target_info[:name]}"
    
    if target_info[:email]
      @results[:email_analysis] = analyze_email_pattern(target_info[:email])
      @results[:email_variations] = generate_email_variations(target_info[:email])
    end

    @results[:psychological_profiling] = psychological_profiling(
      target_info[:name],
      target_info[:email],
      target_info[:company]
    )

    @results[:spear_phishing_templates] = generate_spear_phishing_templates(target_info)

    generate_recommendations

    @results
  end

  def generate_recommendations
    recommendations = []

    case @results[:email_analysis][:pattern_type]
    when 'first.last'
      recommendations << "Use formal communication style"
    when 'firstlast', 'flast'
      recommendations << "Use practical, direct communication"
    end

    case @results[:psychological_profiling][:communication_style]
    when 'formal'
      recommendations << "Maintain professional tone"
    when 'practical'
      recommendations << "Focus on actionable items"
    end

    @results[:recommendations] = recommendations
  end

  def save_results(filename = nil)
    filename ||= "apt_se_analysis_#{Time.now.strftime('%Y%m%d_%H%M%S')}.json"
    
    File.write(filename, JSON.pretty_generate(@results))
    puts "[+] Results saved to: #{filename}"
    filename
  end

  def print_results
    puts "\n[*] Social Engineering Analysis Results:"
    puts "=" * 50

    if @results[:email_analysis]
      puts "\nEmail Analysis:"
      puts "  Email: #{@results[:email_analysis][:email]}"
      puts "  Pattern: #{@results[:email_analysis][:pattern_type]}"
      puts "  Confidence: #{(@results[:email_analysis][:confidence] * 100).round}%"
    end

    if @results[:psychological_profiling]
      puts "\nPsychological Profile:"
      @results[:psychological_profiling].each do |key, value|
        puts "  #{key.to_s.gsub('_', ' ').capitalize}: #{value}"
      end
    end

    if @results[:recommendations] && !@results[:recommendations].empty?
      puts "\nRecommendations:"
      @results[:recommendations].each do |rec|
        puts "  • #{rec}"
      end
    end
  end
end

# CLI Interface
if __FILE__ == $0
  se = APTSocialEngineering.new
  se.print_banner

  if ARGV.empty? || ARGV.include?('--help')
    puts "\nUsage: ruby apt_social_engineering.rb [OPTIONS]"
    puts "\nOPTIONS:"
    puts "  --name NAME          Target's full name"
    puts "  --email EMAIL        Target's email address"
    puts "  --company COMPANY    Target's company"
    puts "  --output FILE        Save results to JSON file"
    puts "  --help              Show this help message"
    puts "\nEXAMPLES:"
    puts "  ruby apt_social_engineering.rb --name 'John Doe' --email john.doe@example.com"
    puts "  ruby apt_social_engineering.rb --email jdoe@company.com --company 'ACME Corp'"
    exit 0
  end

  target_info = {}
  output_file = nil

  ARGV.each_with_index do |arg, i|
    case arg
    when '--name'
      target_info[:name] = ARGV[i + 1]
    when '--email'
      target_info[:email] = ARGV[i + 1]
    when '--company'
      target_info[:company] = ARGV[i + 1]
    when '--output'
      output_file = ARGV[i + 1]
    end
  end

  if target_info.empty?
    puts "[-] Please provide target information (name, email, or company)"
    exit 1
  end

  results = se.analyze_target(target_info)
  se.print_results
  
  if output_file
    se.save_results(output_file)
  end

  puts "\n[+] Analysis completed successfully"
end